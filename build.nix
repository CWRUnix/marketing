{ stdenv, imagemagick, envsubst, python3Full, zip, util-linux, inkscape, dejavu_fonts, xmlstarlet, nerd-fonts, ... }:
stdenv.mkDerivation {
  pname = "CWRUnixBranding";
  version = "1.0.1";

  src = ./.;

  nativeBuildInputs = [
    imagemagick
    envsubst
    python3Full
    zip
    util-linux
    inkscape
    xmlstarlet
    
    dejavu_fonts
    nerd-fonts.fira-code
  ];

  buildPhase = ''
    python build.py
  '';

  installPhase = ''
    mkdir -p $out
    cp -r out/source/* $out
  '';
}
