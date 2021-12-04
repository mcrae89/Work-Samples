// Nate Mead
// Midterm
// CSC 161

public class Movie extends Entertainment {
	private String rating;
	
	// Constructor
	public Movie(String t, String g, String m) throws Exception {
		super(t, g);
		setRating(m);
	}
	
	// Getters/Setters
	
	public String getRating() {
		return this.rating;
	}
	
	public void setRating(String m) throws Exception {
		if (m.toUpperCase().equals("G") || m.toUpperCase().equals("PG") || m.toUpperCase().equals("PG13") || m.toUpperCase().equals("R")) {
			this.rating = m.toUpperCase();
		} else {
			throw new Exception("Improper rating");
		}
	}
	
	@Override
	public String toString() {
		String s = this.getTitle() + " is a movie and is rated " + this.getRating();
		return s;
	}
	
	@Override
	public int compareTo(Entertainment a) {
		return this.getTitle().compareTo(a.getTitle());
	}
}
