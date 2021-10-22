package SubWay2;

import java.util.ArrayList;
import java.util.List;

public class Line {
	//集合保存线路信息
	public static List<Station> line = new ArrayList<Station>();

	public static List<Station> getLine() {
		return line;
	}

	public static void setLine(List<Station> line) {
		Line.line = line;
	}

}
