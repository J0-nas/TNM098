import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import javax.imageio.ImageIO;

public class Lab3_1 {
	public static List<HashMap <Integer, Double>> getHistogramsOfSubImage(BufferedImage im, int x_start, int y_start, int x_offset, int y_offset) {
		if (((x_start - x_offset) > 0) &&
			((x_start + x_offset -1) < im.getWidth()) &&
			((y_start - y_offset) > 0) &&
			((x_start + x_offset -1) < im.getWidth())) {
			x_start = x_start - x_offset;
			y_start = y_start - y_offset;
			x_offset *= 2;
			y_offset *= 2;
			System.out.println("compute histograms of subimage starting at: " + x_start + " - " + y_start + ". x_off: " + x_offset + " y_off: " + y_offset);
			
			BufferedImage subImage = im.getSubimage(x_start, y_start, x_offset, y_offset);
			return getHistograms(subImage);			
		}
		return null;
	}
	
	
	public static List<HashMap <Integer, Double>> getHistograms(BufferedImage im) {
		int height = im.getHeight();
		int width = im.getWidth();
		HashMap<Integer, Double> r = new HashMap<>();
		HashMap<Integer, Double> g = new HashMap<>();
		HashMap<Integer, Double> b = new HashMap<>();
		for (int i = 0; i < 256; i++) {
			r.put(i, 0.0);
			g.put(i, 0.0);
			b.put(i, 0.0);
		}
		
		for (int x = 0; x < width; x++) {
			for (int y = 0; y < height; y++) {
				Color c = new Color(im.getRGB(x, y), true);
				int red = c.getRed();
				double oldRed = r.get(red);
				r.put(red, oldRed + c.getAlpha()*red);
				
				int green = c.getGreen();
				double oldGreen = g.get(green);
				g.put(green, oldGreen + c.getAlpha()*green);
				
				int blue = c.getBlue();
				double oldBlue = b.get(blue);
				b.put(blue, oldBlue + c.getAlpha()*blue);
			}
		}
		ArrayList ret = new ArrayList<HashMap<Integer, Float>>();
		ret.add(r);
		ret.add(g);
		ret.add(b);
		return ret;
	}
	
	public static List<HashMap <Integer, Double>> normalizeHistograms(List<HashMap <Integer, Double>> histograms, BufferedImage im) {
		int size = im.getHeight()*im.getWidth();
		
		for(HashMap<Integer, Double> m : histograms) {
			double max = 0;
			for(double v : m.values()) {
				if (v > max) {
					max = v;
				}
			}
			
			for (int i : m.keySet()) {
				double old = m.get(i);
				m.put(i, (old/size));
			}
		}
		
		return histograms;
	}
	
	public static void printHistogramsToFile(List<HashMap<Integer, Double>> histograms, String filename) {
		 PrintStream printStream;
		try {
			printStream = new PrintStream(new File(filename));
			 for (HashMap<Integer, Double> m : histograms) {
			    	for (int i : m.keySet()) {
			    		//printStream.print(i + " " + m.get(i) + ";");
			    		printStream.print(m.get(i));
			    		//Dont print , before endl
			    		if (i != 255) {
			    			printStream.print(",");
			    		}
			    	}
			    	printStream.print("\n");
			    }
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		BufferedImage im;
		try {
			im = ImageIO.read(new File("02.jpg"));
			List<HashMap<Integer, Double>> histograms = getHistograms(im);
			histograms = normalizeHistograms(histograms, im);
			System.out.println(histograms.get(1));
			
			printHistogramsToFile(histograms, "out2.txt");
			int x = im.getWidth()/2;
			int y = im.getHeight()/2;
			int x_offset = im.getWidth() / 20;
			int y_offset = im.getHeight() / 20;
			
			histograms = getHistogramsOfSubImage(im, x, y, x_offset, y_offset);
			printHistogramsToFile(histograms, "out2_center");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
