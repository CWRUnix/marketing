{ stdenv, imagemagick, envsubst, python3Full, zip, util-linux, inkscape, dejavu_fonts, ... }:
stdenv.mkDerivation {
  pname = "CWRUnixBranding";
  version = "1.0.1";

  src = ./.;

  nativeBuildInputs = [ imagemagick envsubst python3Full zip util-linux inkscape dejavu_fonts ];

  buildPhase = ''
    python build.py
  '';

  installPhase = ''
    mkdir -p $out
    cp -r out/* $out
  '';
}