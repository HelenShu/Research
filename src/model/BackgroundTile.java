package model;
<<<<<<< HEAD
=======
import java.awt.image.BufferedImage;

>>>>>>> 58e4028ae6a41277a892a7ae821401f4457a890b
import javax.swing.ImageIcon;

/**
 * Represents a scenery tile intended to be used as a background tile in the game.
 * A BackgroundTile keeps track of whether or not it can be walked on.  If it can't
 * be walked on then the tile should act as a barrier.
 */
public class BackgroundTile extends Tile {

	private boolean walkable;	// Determines whether this tile can be walked on
	
<<<<<<< HEAD
	public BackgroundTile(ImageIcon icon, String fileName) {
		super(icon, fileName);
		walkable = true;
=======
	public BackgroundTile(BufferedImage icon, String fileName, boolean newWalkable) {
		super(icon, fileName);
		walkable = newWalkable;
>>>>>>> 58e4028ae6a41277a892a7ae821401f4457a890b
	}
	
	public boolean getPropertyWalkable() {
		return walkable;
	}
	
<<<<<<< HEAD
	public void setProertyWalkable(boolean newValue) {
=======
	public void setPropertyWalkable(boolean newValue) {
>>>>>>> 58e4028ae6a41277a892a7ae821401f4457a890b
		walkable = newValue;
	}
	
	@Override
	public String toString() {
		return "[" + getFileName() + " " + walkable + "]";
	}
}