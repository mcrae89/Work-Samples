// Nate Mead
// Midterm
// CSC 161

public class TVShow extends Entertainment {
private String rating;
private String DOTW;
	
	// Constructor
	public TVShow(String t, String g, String m, String d) throws Exception {
		super(t, g);
		setRating(m);
		setDayOfTheWeek(d);
	}
	
	// Getters/Setters
	
	public String getRating() {
		return this.rating;
	}
	
	public void setRating(String m) throws Exception {
		if (m.toUpperCase().equals("TVG") || m.toUpperCase().equals("TVPG") || m.toUpperCase().equals("TV14") || m.toUpperCase().equals("TVMA")) {
			this.rating = m.toUpperCase();
		} else {
			throw new Exception("Improper rating");
		}
	}
	
	public String getDayOfTheWeek() {
		return this.DOTW;
	}
	
	public void setDayOfTheWeek(String d) throws Exception {
		if (d.toUpperCase().equals("SU") || d.toUpperCase().equals("M") || d.toUpperCase().equals("T") || d.toUpperCase().equals("W") || d.toUpperCase().equals("TH")
				|| d.toUpperCase().equals("F") || d.toUpperCase().equals("SA")) {
			this.DOTW = d.toUpperCase();
		} else {
			throw new Exception("Improper Day");
		}
	}
	
	@Override
	public String toString() {
		String s = this.getTitle() + " is a TV Show, is rated " + this.getRating() + " and airs on " + this.getDayOfTheWeek() + " each week.";
		return s;
	}
	
	@Override
	public int compareTo(Entertainment a) {
		return this.getTitle().compareTo(a.getTitle());
	}

}
