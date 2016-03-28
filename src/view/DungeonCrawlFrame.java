package view;
import java.awt.Dimension;

import javax.swing.JFrame;
import javax.swing.JMenuBar;
import javax.swing.JPanel;

import controller.DungeonCrawlController;

public class DungeonCrawlFrame extends JFrame{
	
	JPanel mainPanel;
	JMenuBar menuBar;
	DungeonCrawlController controller;
	
	public DungeonCrawlFrame(DungeonCrawlController myController){
		
		controller = myController;
		
		//Basic window properties
		setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		setTitle("Dungeon Crawler");
		setBounds(300, 100, 600, 670);
		setMinimumSize(new Dimension(800, 670));
		setResizable(false);
		
		mainPanel = new DungeonCrawlView(controller);
		menuBar = new JMenuBar();
		
		this.add(mainPanel);
		this.setVisible(true);
	}
}
