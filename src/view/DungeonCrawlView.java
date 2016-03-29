package view;

import java.awt.BasicStroke;
import java.awt.Graphics;
import java.awt.Graphics2D;

import javax.swing.JPanel;

import controller.DungeonCrawlController;

public class DungeonCrawlView extends JPanel{
	
	DungeonCrawlController controller;
	
	public DungeonCrawlView(DungeonCrawlController newController){
		controller = newController;
	}
	
	public void paintComponent(Graphics g){			
		super.paintComponent(g);
		drawGrid(g);
	}
	
	private void drawGrid(Graphics g){
		for(int y = 0; y < 20; y++){
			for(int x = 0; x < 40; x++){
				g.drawImage(controller.getTileAt(x, y), x*20, y*20, null);
			}
		}
	}
}
