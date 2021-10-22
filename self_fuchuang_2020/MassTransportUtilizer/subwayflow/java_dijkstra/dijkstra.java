package SubWay2;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Scanner;
import java.util.Set;

import SubWay2.ReadFile;
import SubWay2.Station;



public class dijkstra {

	private List<Station> List1 = new ArrayList<Station>();//保存已经遍历过的站点
	//得到与传入参数所有相邻的站点
	private List<Station> getAllNearStations(Station station) {
		List<Station> linkedStaions = new ArrayList<Station>();
		for(List<Station> line : ReadFile.lineSet){//遍历所有线路
			if(line.contains(station)){//当前线路中包含参数站点
				Station s = line.get(line.indexOf(station));//取出当前线路上的该站点的值
				if(s.prevsation != null){
					linkedStaions.add(s.prevsation);//得到当前线路的该站点的前一个站点
				}
				if(s.nextsation != null){
					linkedStaions.add(s.nextsation);//得到当前线路的该站点的后一个站点
				}
			}
		}
		return linkedStaions;
	}
	//得到参数到各个站的最短距离每一站距离为1
	private Station getShortPath(Station station){
		int min = 10000;//定义一个较大的数用做比较
		Station rets = null;
		for(Station s :station.getOrderMap().keySet()){//遍历当前测试站点到所有站点
			if(List1.contains(s)){
				continue;
			}
			LinkedHashSet<Station> set  = station.getAllPassedStations(s);//当前测试站点到未遍历站点的路径
			if(set.size() < min){
				min = set.size();//取路径最短的哪一个
				rets = s;
			}
		}
		return rets;
		//返回最近的这一个站点
	}

	//计算最短经过路径
	public void result(Station s1,Station s2){
		int flag = 0;
		String tempname = "";
		String linename = "";
		//遍历所有站点，判断输入的站名名称是否存在
		int flag1=0;
		for(List<Station> line : ReadFile.lineSet){
			if(line.contains(s1)){
				flag1=1;
			}
		}
		if(flag1==0) {
			System.out.println("输入站点不存在，请重新输入！");
			return ;
		}
		int flag2=0;
		for(List<Station> line : ReadFile.lineSet){
			if(line.contains(s2)){
				flag2=1;
			}
		}
		if(flag2==0) {
			System.out.println("输入站点不存在，请重新输入！");
			return ;
		}
		//当所有站点都遍历完
		if(List1.size() == ReadFile.totalStation){
			System.out.println("起点："+s1.getName()+"  终点站："+s2.getName()+"，共经过"+(s1.getAllPassedStations(s2).size()-1)+"站");
			int p=0;
			for(Station station : s1.getAllPassedStations(s2)){
				//输出遍历s1到s2经过的路径
				p++;
				if(flag == 0) {
					tempname = station.getName();
					// System.out.print("[" + tempname + " -> ");
				}
				else if(flag == 1) {
					linename=station.getLinename();
					System.out.print(station.getLinename() + "-" + tempname + " -> ");
					System.out.print(station.getLinename() + "-" + station.getName() + " -> ");
				}
				else {
					if(!station.getLinename().equals(linename)) {//换乘线路换行输出
						linename=station.getLinename();
						System.out.println();
					}

					if(p<s1.getAllPassedStations(s2).size()) {
						System.out.print(station.getLinename()+"-"+station.getName()+" -> ");
					}else {
						System.out.print(station.getLinename()+"-"+station.getName());
					}
					
				}
				flag++;
			}
			return;
		}
		if(!List1.contains(s1)){//将当前测试站点储存在已遍历链表
			List1.add(s1);
		}
		//如果起点的测试站点的OrderMap为空，则第一次用该站的相邻站点初始化
		if(s1.getOrderMap().isEmpty()){
			List<Station> Linkedstations = getAllNearStations(s1);
			for(Station s : Linkedstations){
				s1.getAllPassedStations(s).add(s);
			}
		}
		Station psation = getShortPath(s1);//获取距离起点站s1最近的一个站
		if(psation == s2){
			System.out.println("找到目标站点："+s2+"，共经过"+(s1.getAllPassedStations(s2).size()-1)+"站");
			for(Station station : s1.getAllPassedStations(s2)){
				System.out.print(station.getName()+" -> ");
			}
			return;
		}
		for(Station station1 : getAllNearStations(psation)){
			if(List1.contains(station1)){
				continue;
			}
			int shortestPath = (s1.getAllPassedStations(psation).size()-1) + 1;//计算所需距离
			if(s1.getAllPassedStations(station1).contains(station1)){
				//如果s1已经计算过到此station1的经过距离，那么比较出最小的距离
				if((s1.getAllPassedStations(station1).size()-1) > shortestPath){
					//重置S1到周围各站的最小路径
					s1.getAllPassedStations(station1).clear();
					s1.getAllPassedStations(station1).addAll(s1.getAllPassedStations(psation));
					s1.getAllPassedStations(station1).add(station1);
				}
			} else {
				//如果s1还没有计算过到此station1的经过距离
				s1.getAllPassedStations(station1).addAll(s1.getAllPassedStations(psation));
				s1.getAllPassedStations(station1).add(station1);
			}
		}
		List1.add(psation);
		result(s1,s2);//重复计算，往外面站点扩展
	}

	public static void main(String[] args) {
		dijkstra subway = new dijkstra();
		ReadFile.readText();

		// Scanner input =new Scanner(System.in);
		// System.out.print("请输入起点：");
		// String str1 = input.next();
		// System.out.print("请输入终点：");
		// String str2 = input.next();
		// input.close();
		// subway.result(new Station(str1), new Station(str2));	
		subway.result(new Station("Sta128"), new Station("Sta65"));	
	}
}
