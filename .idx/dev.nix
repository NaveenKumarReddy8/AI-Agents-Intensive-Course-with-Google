# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-25.11"; # or "unstable"
  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python313
    pkgs.gnumake
  ];
  # Sets environment variables in the workspace
  env = {};
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "ms-python.python"
      "ms-python.debugpy"
    ];
    workspace = {
      # Runs when a workspace is first created with this `dev.nix` file
      onCreate = {
        create-venv = ''
          curl -LsSf https://astral.sh/uv/install.sh | sh
          source $HOME/.local/bin/env
        '';
        # Open editors for the following files by default, if they exist:
        default.openFiles = ["README.md"];
      };
      onStart = {
        install-dependencies = ''
          uv sync --all-groups --all-extras
        '';
      };
      # To run something each time the workspace is (re)started, use the `onStart` hook
    };
    previews = {
      enable = false;
    };
  };
}
