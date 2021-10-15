// Nate Mead
// Midterm
// CSC 161

public abstract class Entertainment implements Comparable<Entertainment> {
	private String title;
	private String genre;
	
	// Constructor
	public Entertainment(String t, String g) {
		setTitle(t);
		setGenre(g);
	}
	
	// Getters/Setters
	public String getTitle() {
		return this.title;
	}
	
	public void setTitle(String t) {
		this.title = t;
	}
	
	public String getGenre() {
		return this.genre;
	}
	
	public void setGenre(String g) {
		this.genre = g;
	}
	
	@Override
	public abstract String toString();
}
