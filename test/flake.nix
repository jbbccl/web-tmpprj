{
  description = "tmpprj dev environment (FastAPI backend + Vue/Vite frontend + local MariaDB)";

  inputs.nixpkgs.url = "nixpkgs";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};

      py = pkgs.python313.withPackages (ps: with ps; [
        fastapi
        uvicorn
        watchfiles
        sqlalchemy
        pymysql
        pyjwt
        python-multipart
      ]);
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = [ py pkgs.nodejs pkgs.mariadb ];

        shellHook = ''
          export PYTHON_INTERPRETER=$(which python)
        '';
      };
    };
}
