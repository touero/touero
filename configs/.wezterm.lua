-- Pull in the wezterm API
local wezterm = require 'wezterm'

-- This table will hold the configuration.
local config = {}

-- In newer versions of wezterm, use the config_builder which will
-- help provide clearer error messages
if wezterm.config_builder then
  config = wezterm.config_builder()
end

-- This is where you actually apply your config choices

-- Changing the color scheme:
config.color_scheme = 'Gruvbox dark, hard (base16)'

-- Adding JetBrains Mono font and set font size
config.font = wezterm.font('JetBrains Mono', { weight = 'Bold'})
config.font_size = 16

-- Set to background opacity
config.window_background_opacity = 0.8

-- Set to borderless mode
config.window_decorations = "NONE"

config.default_cursor_style = "BlinkingBar"
config.cursor_blink_rate = 500

config.initial_rows = 43
config.initial_cols = 90

-- and finally, return the configuration to wezterm
return config
