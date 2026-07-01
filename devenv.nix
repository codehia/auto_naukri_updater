{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/packages/
  packages = with pkgs; [ git firefox-esr ];

  # https://devenv.sh/languages/
  languages.python = {
    enable = true;
    poetry.enable = true;
  };

}
