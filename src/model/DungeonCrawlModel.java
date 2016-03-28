package model;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Scanner;

import javax.imageio.ImageIO;

import controller.DungeonCrawlController;

public class DungeonCrawlModel {

	private BackgroundTile[][] background = new BackgroundTile[20][40];
	DungeonCrawlController controller;
	
	File imagesFolder = new File("images");
	File levelsFolder = new File("levels");
	
	int characterX;
	int characterY;

	public DungeonCrawlModel(DungeonCrawlController newController){
		controller = newController;
	}
	
	public void loadLevel(String levelName){
		try{
			File f = null;
			for(final File files : levelsFolder.listFiles()){
				if(files.getName().equals(levelName)){
					f = files;
				}
			}
			if(f != null){
				Scanner row = new Scanner(f);
				int x = 0;
				int y = 0;
				while(row.hasNextLine()){
					
					Scanner col = new Scanner(row.nextLine());
					
					while(col.hasNext()){
						
						String imageName = col.next();
						boolean walkable = col.next().equals("true");
						setTileAt(x,y,imageName, walkable);
						x++;
						
					}
					x = 0;
					y++;
					col.close();
				}
				row.close();
			}
		}catch(IOException i){
			System.out.println("Error: " + i.getMessage());
		}
	}
	
	public void setTileAt(int x, int y, String fileName, boolean walkable){
		try{
			File f = null;
			for(final File files : imagesFolder.listFiles()){
				if(files.getName().equals(fileName)){
					f = files;
				}
			}
			BufferedImage image = ImageIO.read(f);
			background[y][x] = new BackgroundTile(image, fileName, walkable);
		}catch(IOException i){
			
		}
	}
	
	public int getCharacterXPos(){
		return 0;
	}
	
	public int getCharacterYPos(){
		return 0;
	}
	
	public BackgroundTile[][] getBackground(){
		return background;
	}
}
