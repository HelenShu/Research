package controller;

import model.BackgroundTile;
import model.DungeonCrawlModel;
import model.Tile;
import view.DungeonCrawlFrame;
import view.DungeonCrawlView;

import java.awt.Image;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.File;

import javax.imageio.ImageIO;

public class DungeonCrawlController implements KeyListener {

	DungeonCrawlModel model;
	DungeonCrawlFrame view;
	
	final String NUMBER_FILE_END = ".gif";
	
	public DungeonCrawlController(){
		model = new DungeonCrawlModel(this);
		model.loadLevel("level1");
		view = new DungeonCrawlFrame(this);
	}
	
	public Image getTileAt(int x, int y){
		return model.getBackground()[y][x].getImage();
	}

	@Override
	public void keyPressed(KeyEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void keyReleased(KeyEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void keyTyped(KeyEvent e) {
		int x = model.getCharacterXPos();
		int y = model.getCharacterYPos();

		// 'c' means that that is where the character is located
		if (e.getKeyCode() == KeyEvent.VK_UP) {
			if (x != 0){
				//model.getGrid()[x - 1][y] = 'c';
			}
		}
		if (e.getKeyCode() == KeyEvent.VK_DOWN) {
			if (x != model.getBackground().length - 1){
				//model.getGrid()[x + 1][y] = 'c';
			}
		}
		if (e.getKeyCode() == KeyEvent.VK_LEFT) {
			if (y != 0){
				//model.getGrid()[x][y - 1] = 'c';
			}
		}
		if (e.getKeyCode() == KeyEvent.VK_RIGHT) {
			if (y != model.getBackground()[0].length - 1){
				//model.getGrid()[x][y + 1] = 'c';
			}
		}

	}

}
