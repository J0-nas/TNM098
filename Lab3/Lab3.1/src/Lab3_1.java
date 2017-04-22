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
				r.put(red, oldRed + c.getAlpha());
				
				int green = c.getGreen();
				double oldGreen = g.get(green);
				g.put(green, oldGreen + c.getAlpha());
				
				int blue = c.getBlue();
				double oldBlue = b.get(blue);
				b.put(blue, oldBlue + c.getAlpha());
			}
		}
		ArrayList ret = new ArrayList<HashMap<Integer, Float>>();
		ret.add(r);
		ret.add(g);
		ret.add(b);
		return ret;
	}
	
	public static List<HashMap <Integer, Double>> normalizeHistograms(List<HashMap <Integer, Double>> histograms, int size) {		
		for(HashMap<Integer, Double> m : histograms) {
//			double max = 0;
//			for(double v : m.values()) {
//				if (v > max) {
//					max = v;
//				}
//			}
//			
			for (int i : m.keySet()) {
				double old = m.get(i);
				m.put(i, (old/size)*10);
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
		if (args.length == 0) {
			System.out.println("No filenames provided...");
			return;
		}
		for (int i = 0; i<args.length; i++) {
			// TODO Auto-generated method stub
			BufferedImage im;
			//String id = "01";
			String id = args[i];
			try {
				
				im = ImageIO.read(new File(id + ".jpg"));
				List<HashMap<Integer, Double>> histograms = getHistograms(im);
				histograms = normalizeHistograms(histograms, im.getWidth()*im.getHeight());
				System.out.println(histograms.get(1));
				printHistogramsToFile(histograms, "out_" + id);
				
				// take w/10 and h/10 pixels left, right, above, below the x-y point
				int frame_width = 10;
				int frame_height = 10;
				int x = im.getWidth()/2;
				int y = im.getHeight()/2;
				int x_offset = im.getWidth() / frame_width;
				int y_offset = im.getHeight() / frame_height;
				int frame_size = 2*x_offset * 2*y_offset;
				histograms = getHistogramsOfSubImage(im, x, y, x_offset, y_offset);
				histograms = normalizeHistograms(histograms, frame_size);
				printHistogramsToFile(histograms, "out_center_" + frame_width + "-" + frame_height + "_" + id);
				
				int x_0 = im.getWidth()/4;
				int x_1 = (im.getWidth()/4) * 3;
				int y_0 = im.getHeight()/4;
				int y_1 = (im.getHeight()/4) * 3;
				histograms = getHistogramsOfSubImage(im, x_0, y_0, x_offset, y_offset);
				histograms = normalizeHistograms(histograms, frame_size);
				printHistogramsToFile(histograms, "out_0-0_" + id);
				histograms = getHistogramsOfSubImage(im, x_0, y_1, x_offset, y_offset);
				histograms = normalizeHistograms(histograms, frame_size);
				printHistogramsToFile(histograms, "out_0-1_" + id);
				histograms = getHistogramsOfSubImage(im, x_1, y_0, x_offset, y_offset);
				histograms = normalizeHistograms(histograms, frame_size);
				printHistogramsToFile(histograms, "out_1-0_" + id);
				histograms = getHistogramsOfSubImage(im, x_1, y_1, x_offset, y_offset);
				histograms = normalizeHistograms(histograms, frame_size);
				printHistogramsToFile(histograms, "out_1-1_" + id);
				
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
}
