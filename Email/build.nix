{ stdenv, envsubst, python3Full, inkscape, ... }:
stdenv.mkDerivation {
  pname = "CWRUnixBranding";
  version = "1.0.1";

  src = ./.;

  nativeBuildInputs = [ envsubst python3Full inkscape ];

  buildPhase = ''
    python build.py
  '';

  installPhase = ''
    mkdir -p $out
    cp -r out/* $out
  '';
}