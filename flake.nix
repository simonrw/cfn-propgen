{
  description = "Flake utils demo";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        overlays = [
        ];

        pkgs = import nixpkgs {
          inherit overlays system;
        };
      in
      {
        devShells = rec {
          default = python-dev;

          python-dev = pkgs.mkShell {
            buildInputs = with pkgs; [
              pkgs.python3
              pkgs.python3.pkgs.venvShellHook
            ];

            venvDir = ".venv";

            postVenvCreation = ''
              python -m pip install pip-tools
            '';
          };
        };
      }
    );
}
