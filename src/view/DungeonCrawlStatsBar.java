package view;

import java.awt.event.MouseListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;
import javax.swing.Icon;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;

import controller.DungeonCrawlController;

//this is to show the status bar and skills of the player character; located beneath the playing grid
public class DungeonCrawlStatsBar extends JPanel {

	// i...guess I'll wait for I to draw those pictures first
	// I'm pretty sure I need the controller to be a mouseListener for this

	DungeonCrawlController controller;

	JPanel healthBar;
	JLabel health = new JLabel("Health");
	JPanel manaBar;
	JLabel mana = new JLabel("Mana");

	JButton spell1;
	JButton spell2;
	JButton spell3;

	JButton skills1;
	JButton skills2;
	JButton skills3;
	JButton skills4;
	JButton skills5;

	public DungeonCrawlStatsBar(DungeonCrawlController newController) {
		controller = newController;
		healthBar();
		manaBar();
		spells();
		skillsButton();
	}

	// one int for max health, one int for current health
	public void healthBar() {
		healthBar = new JPanel();
		healthBar.add(health);
		// assuming you start with 3 health
		try {
			BufferedImage image = ImageIO.read(new File("images/Dirt.gif"));
			JLabel pic = new JLabel((Icon) image);
			for (int i = 0; i < 3; i++) {
				healthBar.add(pic);
			}

		} catch (IOException e) {
			e.getMessage();
		}

		this.add(healthBar);
	}

	// changes health bar to reflect current health....somehow
	public void changeHealth(int max, int current) {
		int used = max - current;
		healthBar.removeAll();
		healthBar.add(health);
		for(int i = 0; i < max; i++){
			try {
				BufferedImage image = ImageIO.read(new File("images/Dirt.gif"));
				BufferedImage image2 = ImageIO.read(new File("images/DirtWall.gif"));
				JLabel avai = new JLabel((Icon) image);
				JLabel hit = new JLabel((Icon) image2);
				if(i < current){
					healthBar.add(avai);
				}else {
					healthBar.add(hit);
				}
			} catch (IOException e) {
				e.getMessage();
			}	
		}
	}

	// one int for max mana, one int for current mana
	public void manaBar() {
		manaBar = new JPanel();
		manaBar.add(mana);
		// assuming you start with 3 mana
		try {
			BufferedImage image = ImageIO.read(new File("images/Dirt.gif"));
			JLabel pic = new JLabel((Icon) image);
			for (int i = 0; i < 3; i++) {
				manaBar.add(pic);
			}

		} catch (IOException e) {
			e.getMessage();
		}
		this.add(manaBar);
	}

	// changes mana bar to reflect current mana....somehow
	public void changeMana(int max, int current) {
		int used = max - current;
		manaBar.removeAll();
		manaBar.add(mana);
		for(int i = 0; i < max; i++){
			try {
				BufferedImage image = ImageIO.read(new File("images/Dirt.gif"));
				BufferedImage image2 = ImageIO.read(new File("images/DirtWall.gif"));
				JLabel avai = new JLabel((Icon) image);
				JLabel hit = new JLabel((Icon) image2);
				if(i < current){
					manaBar.add(avai);
				}else {
					manaBar.add(hit);
				}
			} catch (IOException e) {
				e.getMessage();
			}	
		}
	}

	// buttons you press to use spells
	public void spells() {
		JPanel accessSpells = new JPanel();
		try {
			BufferedImage image = ImageIO.read(new File("images/Dirt.gif"));
			spell1 = new JButton((Icon) image);
			spell2 = new JButton((Icon) image);
			spell3 = new JButton((Icon) image);

			accessSpells.add(spell1);
			accessSpells.add(spell2);
			accessSpells.add(spell3);
		} catch (IOException e) {

		}
		this.add(accessSpells);
	}

	// will somehow show the cooldown on spells, just not really sure how
	public void cooldownSpell() {

	}

	public void setMouseListener(MouseListener controller) {
		spell1.addMouseListener(controller);
		spell2.addMouseListener(controller);
		spell3.addMouseListener(controller);
		skills1.addMouseListener(controller);
		skills2.addMouseListener(controller);
		skills3.addMouseListener(controller);
		skills4.addMouseListener(controller);
		skills5.addMouseListener(controller);
	}

	// button for accessing point allocation menu; dunno how many skills we have
	// so I made five, three for the spells, and two extra
	public void skillsButton() {
		JPanel updateSkills = new JPanel();
		JButton skills1 = new JButton("Unlock (name of spell 1): ___ points");
		JButton skills2 = new JButton("Unlock (name of spell 2): ___ points");
		JButton skills3 = new JButton("Unlock (name of spell 3): ___ points");
		JButton skills4 = new JButton("Unlock skill 4: ___ points");
		JButton skills5 = new JButton("Unlock skill 5: ___ points");

		updateSkills.add(skills1);
		updateSkills.add(skills2);
		updateSkills.add(skills3);
		updateSkills.add(skills4);
		updateSkills.add(skills5);

		this.add(updateSkills);
	}
}