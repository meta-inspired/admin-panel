{
  description = "Salt+Light admin panel created with Streamlit";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";

    flake-parts.url = "github:hercules-ci/flake-parts";

    pyproject.url = "github:nix-community/pyproject.nix";
  };

  outputs = {
    flake-parts,
    pyproject,
    ...
  } @ inputs:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = inputs.nixpkgs.lib.systems.flakeExposed;

      perSystem = {
        pkgs,
        system,
        ...
      }: let
        project = inputs.pyproject.lib.project.loadRequirementsTxt {
          projectRoot = ./.;
        };

        python = pkgs.python311;

        firebase-admin = pkgs.python311Packages.buildPythonPackage rec {
          pname = "firebase_admin";
          version = "6.2.0";
          src = pkgs.fetchPypi {
            inherit pname version;
            sha256 = "sha256-47M00Yu+oDny8+inkq1ocNKnzHmhPtEGWd7dY/W0deQ=";
          };
          doCheck = false;
        };

        overlay = final: prev: {
          pythonPackages311Overlays =
            (prev.pythonPackages311Overlays or [])
            ++ [
              (python-final: python-prev: {
                inherit firebase-admin;
              })
            ];

          python311 = let
            self = prev.python311.override {
              inherit self;
              packageOverrides = prev.lib.composeManyExtensions final.pythonPackages311Overlays;
            };
          in
            self;

          python311Packages = final.python311.pkgs;
        };

        pythonEnv = pkgs.python311.withPackages (project.renderers.withPackages {inherit python;});
      in {
        _module.args.pkgs = import inputs.nixpkgs {
          inherit system;
          overlays = [overlay];
        };

        devShells.default = pkgs.mkShell {
          name = "saltandlight-admin-panel-shell";
          packages = [
            pythonEnv
          ];
        };
      };
    };
}
