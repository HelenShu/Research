package model;
import java.awt.Image;
<<<<<<< HEAD
=======
import java.awt.image.BufferedImage;
>>>>>>> 58e4028ae6a41277a892a7ae821401f4457a890b

import javax.swing.ImageIcon;

/**
 * This class represents a graphical Tile in the game.
 * If you use it, you should EXTEND it or ADD MORE PROPERTIES
 */
public class Tile  {

<<<<<<< HEAD
	private ImageIcon icon;		// Graphical representation of this tile
	private String fileName;	// Filename should match the ImageIcon used
	
	public Tile(ImageIcon icon, String fileName) {
		this.icon = icon;
		this.fileName = fileName;
	}
	
	public ImageIcon getImageIcon() {
		return icon;
	}

	public Image getImage() {
		return icon.getImage();
=======
	private BufferedImage image;		// Graphical representation of this tile
	private String fileName;	// Filename should match the ImageIcon used
	
	public Tile(BufferedImage image, String fileName) {
		this.image = image;
		this.fileName = fileName;
	}
	
	public BufferedImage getImage() {
		return image;
>>>>>>> 58e4028ae6a41277a892a7ae821401f4457a890b
	}
	
	public String getFileName() {
		return fileName;
	}

	@Override
	public String toString() {
		return "[" + fileName + "]";
	}
}