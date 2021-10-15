// Nate Mead
// Midterm
// CSC 161

import java.util.ArrayList;
import java.util.Collections;
import java.util.InputMismatchException;
import java.util.Scanner;

public class MidtermProgram {
	// Global scanner
	static Scanner input = new Scanner(System.in);
	
	public static void main(String[] args) throws Exception {
		ArrayList<Entertainment> list = new ArrayList<Entertainment>();
		
		boolean quit = false;
		
		while (!quit) {
			// menu set up
			System.out.println("Please enter a number from the list: \n1) Add \n2) Remove \n3) See list \n4) Search \n5) Quit");
			try {
				int selection = input.nextInt();
				switch(selection) {
				case(5):
					quit = true;
					break;
				case(1):
					System.out.println();
					addEntertainment(list);
					System.out.println();
					break;
				case(2):
					System.out.println();
					removeEntertainment(list);
					System.out.println();
					break;
				case(3):
					System.out.println();
					seeList(list);
					System.out.println();
					break;
				case(4):
					System.out.println();
					searchList(list);
					System.out.println();
					break;
				default:
					System.out.println("Selection entered was incorrect. Please try again.");
					System.out.println();
					break;
				}	
			} catch (InputMismatchException e) {
				System.out.println("Selection entered was incorrect. Please try again.");
				input.nextLine();
				System.out.println();
			}
		}
		
		input.close();
	}
	
	// adds a new object to the list
	public static void addEntertainment(ArrayList<Entertainment> l) {
		System.out.println("Please select what type of entertainment you would like to add: Movie or TV");
		String e = input.next();
		input.nextLine();
		if (e.toUpperCase().equals("MOVIE") || e.toUpperCase().equals("TV")) {
			System.out.print("Please enter the title: ");
			String t = input.nextLine();
			System.out.print("Please enter the genre: ");
			String g = input.next();
			if (e.toUpperCase().equals("MOVIE")) {
				try {
					System.out.println("Please enter an age rating: (G, PG, PG13, or R)");
					String r = input.next().toUpperCase();
					l.add(new Movie(t, g, r));
				} catch (Exception r) {
					System.out.println("Rating exception: " + r.getMessage()); 
					System.out.println();
				}
			} else if (e.toUpperCase().equals("TV")) {
				try{
					System.out.println("Please enter an age rating: (TVG, TVPG, TV14, or MA)");
					String r = input.next().toUpperCase();
					System.out.println("Please enter the day of the week that this show airs: (SU, M, T, W, TH, F, SA)");
					String d = input.next().toUpperCase();
					l.add(new TVShow(t, g, r, d));
				} catch (Exception d) {
					System.out.println(d.getMessage());
					System.out.println();
				} 
			} 
		} else {
			System.out.println("Improper selection");
		}
	}
	
	// removes an object from to list or returns empty
	public static void removeEntertainment(ArrayList<Entertainment> l) {
		if (l.isEmpty()) {
			System.out.println("The list is empty");
		} else {
			System.out.println("Please enter a title to remove");
			input.nextLine();
			String e = input.nextLine();
			for (int i = 0; i <= l.size(); i++) {
				if (e.toUpperCase().equals(l.get(i).getTitle().toUpperCase())) {
					l.remove(i);
				} else {
					System.out.println(e + " was not found.");
				}
			}
		}
	}
	
	// searches a list for an object or returns empty
	public static void searchList(ArrayList<Entertainment> l) {
		boolean found = false;
		if (l.isEmpty()) {
			System.out.println("The list is empty");
		} else {
			Collections.sort(l);
			System.out.println("Please enter a title to search for: ");
			input.nextLine();
			String e = input.nextLine();
			for (int i = 0; i < l.size(); i++) {
				if (e.toUpperCase().equals(l.get(i).getTitle().toUpperCase())) {
					found = true;
					break;
				}
			}
			if (found == true) {
				System.out.println(e + " was found");
			} else {
				System.out.println(e + " was not found");
			}
		}
	}
	
	// prints the list or returns empty
	public static void seeList(ArrayList<Entertainment> l) {
		if (l.isEmpty()) {
			System.out.println("The list is empty");
		} else {
			for (int i = 0; i < l.size(); i++) {
				System.out.println(i+1 + ". " + l.get(i));
		}
		}
	}
}
