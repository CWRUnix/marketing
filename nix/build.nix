{ stdenv, imagemagick, envsubst, python3Full, zip, util-linux, inkscape-with-extensions, dejavu_fonts, xmlstarlet, nerd-fonts, gnutar,
  tar ? false, 
  ... }:
stdenv.mkDerivation {
  pname = "CWRUnixBranding";
  version = "1.0.1";

  src = ./..;

  nativeBuildInputs = [
    imagemagick
    envsubst
    python3Full
    zip
    util-linux
    inkscape-with-extensions
    xmlstarlet
    
    dejavu_fonts
    nerd-fonts.fira-code
    gnutar
  ];

  buildPhase = ''
    set -euxo pipefail
    mkdir -p ./out

    # Make home for inkscape
    export HOME=$(realpath ./home)
    mkdir -p $HOME

    python build.py
  '';

  installPhase = ''
    mkdir -p $out
  '' + (if tar then "tar -czvf $out/media.tgz out/source/*" else "cp -r out/source/* $out");
}