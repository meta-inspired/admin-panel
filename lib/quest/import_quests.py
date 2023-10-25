import argparse
import io
import os
from contextlib import redirect_stdout
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from firebase_admin import firestore
from google.cloud.firestore import Client as FirestoreClient


def import_journeys(db: FirestoreClient, worksheet: Worksheet) -> None:
    for row in range(4, worksheet.max_row):
        column_names = {}
        current = 1
        columns = worksheet.iter_cols(min_col=0, min_row=3, max_col=worksheet.max_column, max_row=3)
        for column in columns:
            column_names[column[0].value] = current
            current += 1

        journey_id = worksheet.cell(row, column_names["EveryQuestJourney"]).value

        if journey_id is None:
            break

        choices = []
        data = {
            "after": "",
            "before": "",
            "chapterID": worksheet.cell(row, column_names["EveryQuestChapter"]).value,
            "contentType": worksheet.cell(row, column_names["EveryQuestContenttype"]).value,
            "journeyID": journey_id,
            "title": worksheet.cell(row, column_names["EveryQuestTitle"]).value,
            "tooltipEmoji": worksheet.cell(row, column_names["TooltipManagementTooltipemoji"]).value,
            "successTooltip": worksheet.cell(row, column_names["TooltipManagementTooltiptext"]).value,
        }

        quest_type = worksheet.cell(row, column_names["EveryQuestContenttype"]).value

        if quest_type == "video":
            data["title"] = worksheet.cell(row, column_names["EveryQuestTitle"]).value
            data["video"] = {
                "duration": 0,
                "thumbnailURL": worksheet.cell(row, column_names["VideoQuestThumbnailurl"]).value,
                "url": worksheet.cell(row, column_names["VideoQuestVideourl"]).value,
            }

        elif quest_type == "riff":
            data["title"] = worksheet.cell(row, column_names["EveryQuestTitle"]).value
            data["riff"] = {
                "question": worksheet.cell(row, column_names["RiffQuestion"]).value,
                "tip": worksheet.cell(row, column_names["RiffTip"]).value,
            }

        elif quest_type == "multiChoiceQuestion":
            for index in range(0, 6):
                if worksheet.cell(row, index + column_names["MultiChoiceAndMultiChoiceAnswerChoice1"]).value:
                    option = worksheet.cell(
                        row,
                        index + column_names["MultiChoiceAndMultiChoiceAnswerChoice1"],
                    ).value
                    choice = {
                        "id": index,
                        "option": option,
                    }
                    choices.append(choice)

            data["answerQuestID"] = worksheet.cell(row, column_names["AnswerQuestID"]).value
            data["question"] = {"choices": choices}

            correct_answer = str(
                worksheet.cell(row, column_names["MultiChoiceAndMultiChoiceAnswerCorrectAnswer"]).value
            )
            if not correct_answer:
                if "," not in correct_answer:
                    correct_answer = [int(correct_answer) - 1]
                else:
                    correct_answer = correct_answer.split(",")
                    # subtract 1 from the correct answer elements for zero based indexing
                    correct_answer = [int(x) - 1 for x in correct_answer]
                data["correctAnswer"] = correct_answer

        elif quest_type == "multiChoiceAnswer":
            for index in range(0, 6):
                if worksheet.cell(row, index + column_names["MultiChoiceAndMultiChoiceAnswerChoice1"]).value:
                    choice = {
                        "id": index,
                        "option": worksheet.cell(
                            row,
                            index + column_names["MultiChoiceAndMultiChoiceAnswerChoice1"],
                        ).value,
                        "totalAnswer": 0,
                    }
                    choices.append(choice)

            data["total"] = 0
            data["question"] = {"choices": choices}

        elif quest_type == "message":
            data["imageUrl"] = worksheet.cell(row, column_names["MessageQuestImageurl"]).value
            data["body"] = worksheet.cell(row, column_names["MessageQuestBody"]).value

        elif quest_type == "communityResponse":
            data["title"] = worksheet.cell(row, column_names["QuestionCommunityResponse"]).value

        elif quest_type == "madlib":
            data["question"] = worksheet.cell(row, column_names["MadLibQuestion"]).value

        elif quest_type == "tapAndDrag":
            choicesList = str(worksheet.cell(row, column_names["Tap&DragAnswers"]).value).split(",")
            choices = []
            for index in range(0, len(choicesList)):
                choice = {"id": index, "text": choicesList[index]}
                choices.append(choice)

            zones = []
            for index in range(0, 3):
                if worksheet.cell(row, index + column_names["Tap&DragId1"]).value:
                    zone = {
                        "id": index,
                        "text": worksheet.cell(row, index + column_names["Tap&DragId1"]).value,
                    }
                    zones.append(zone)

            data["answers"] = choices
            data["zones"] = zones

        else:
            # invalid quest type found, skip uploading
            print(f"\nwarning: invalid quest type, found '{quest_type}': skipping upload")
            continue

        chapter_id = str(worksheet.cell(row, column_names["EveryQuestChapter"]).value)
        quest_id = str(worksheet.cell(row, column_names["EveryQuestId"]).value)

        path = f"journeys/{journey_id}/chapters/{chapter_id}/quests"
        print(f"\n{path}/{quest_id}")
        db.collection(path).document(quest_id).set(data)


def import_journey_metadata(db: FirestoreClient, worksheet: Worksheet) -> None:
    column_names = {}
    current = 1

    for column in worksheet.iter_cols(min_col=0, min_row=1, max_col=worksheet.max_column, max_row=1):
        column_names[column[0].value] = current
        current += 1

    for row in range(2, worksheet.max_row):
        journey_id = worksheet.cell(row, column_names["journey"]).value
        chapter_id = worksheet.cell(row, column_names["chapter"]).value

        if journey_id is None:
            break

        data = {
            "name": worksheet.cell(row, column_names["name"]).value,
            "chapterNumber": worksheet.cell(row, column_names["chapterNumber"]).value,
            "author": worksheet.cell(row, column_names["author"]).value,
            "title": worksheet.cell(row, column_names["Title"]).value,
            "subTitle": worksheet.cell(row, column_names["subTitle"]).value,
            "description": worksheet.cell(row, column_names["description"]).value,
            "image": worksheet.cell(row, column_names["image"]).value,
        }

        path = f"journeys/{journey_id}/chapters"
        print(f"\n{path}/{chapter_id}")
        db.collection(path).document(str(chapter_id)).set(data)


def import_quests(import_file):
    db = firestore.client()
    with io.StringIO() as buffer, redirect_stdout(buffer):
        worksheet_filename = import_file
        workbook = load_workbook(worksheet_filename)

        journey_worksheet_name = "journey_data"
        journey_metadata_worksheet_name = "chapter_metadata"

        journey_worksheet = workbook[journey_worksheet_name]
        journey_metadata_worksheet = workbook[journey_metadata_worksheet_name]

        print("Importing journeys...")
        import_journeys(db, journey_worksheet)

        print("\nImporting journey metadata...")
        import_journey_metadata(db, journey_metadata_worksheet)

        print("\nFinished import!")
        output = buffer.getvalue()
    return output

