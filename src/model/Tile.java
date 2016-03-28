package model;
import java.awt.Image;
import java.awt.image.BufferedImage;

import javax.swing.ImageIcon;

/**
 * This class represents a graphical Tile in the game.
 * If you use it, you should EXTEND it or ADD MORE PROPERTIES
 */
public class Tile  {

	private BufferedImage image;		// Graphical representation of this tile
	private String fileName;	// Filename should match the ImageIcon used
	
	public Tile(BufferedImage image, String fileName) {
		this.image = image;
		this.fileName = fileName;
	}
	
	public BufferedImage getImage() {
		return image;
	}
	
	public String getFileName() {
		return fileName;
	}

	@Override
	public String toString() {
		return "[" + fileName + "]";
	}
}