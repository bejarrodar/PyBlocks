import tkinter as tk
from unittest.mock import MagicMock, patch
from pyblocks.app import PyBlocksApp

class TestAppChallenge:
    @patch("pyblocks.app.PyBlocksApp._build_menu")
    @patch("pyblocks.app.PyBlocksApp._build_toolbar")
    @patch("pyblocks.app.PyBlocksApp._build_layout")
    @patch("pyblocks.app.PyBlocksApp._bind_keys")
    @patch("tkinter.Tk.title")
    @patch("tkinter.Tk.geometry")
    @patch("tkinter.Tk.protocol")
    def test_show_challenge_calls_popup(self, mock_proto, mock_geom, mock_title, 
                                         mock_bind, mock_layout, mock_toolbar, mock_menu):
        with patch("pyblocks.app.PyBlocksApp.__init__", return_value=None):
            app = PyBlocksApp()
            app._project = MagicMock()
            app._canvas_panel = MagicMock()
            app._on_close = MagicMock()

            with patch("pyblocks.challenges.bank.ChallengeBank.load") as mock_load, \
                 patch("pyblocks.ui.challenge_popup.ChallengePopup") as MockPopup:
                
                mock_challenge = MagicMock()
                mock_bank = MagicMock()
                mock_bank.random.return_value = mock_challenge
                mock_load.return_value = mock_bank
                
                app._show_challenge()

                mock_load.assert_called_once()
                mock_bank.random.assert_called_once()
                MockPopup.assert_called_once_with(
                    app, challenge=mock_challenge, on_accept=app._apply_starter_block
                )

    @patch("pyblocks.app.PyBlocksApp._build_menu")
    @patch("pyblocks.app.PyBlocksApp._build_toolbar")
    @patch("pyblocks.app.PyBlocksApp._build_layout")
    @patch("pyblocks.app.PyBlocksApp._bind_keys")
    @patch("tkinter.Tk.title")
    @patch("tkinter.Tk.geometry")
    @patch("tkinter.Tk.protocol")
    def test_apply_starter_block(self, mock_proto, mock_geom, mock_title, 
                                  mock_bind, mock_layout, mock_toolbar, mock_menu):
        with patch("pyblocks.app.PyBlocksApp.__init__", return_value=None):
            app = PyBlocksApp()
            app._project = MagicMock()
            # Manually set up the canvas panel and its renderer to avoid nested mock issues
            mock_model = MagicMock()
            mock_model.blocks = []
            
            app._canvas_panel = MagicMock()
            app._canvas_panel.renderer = MagicMock()
            app._canvas_panel.renderer._model = mock_model

            challenge = MagicMock()
            challenge.starter_comment = "Hello"
            
            with patch.object(app, "_on_canvas_change"):
                app._apply_starter_block(challenge)
            
            assert len(app._canvas_panel.renderer._model.blocks) == 1
            assert app._canvas_panel.renderer._model.blocks[0].type == "comment_block"
            assert app._canvas_panel.renderer._model.blocks[0].label_template == "Hello"
