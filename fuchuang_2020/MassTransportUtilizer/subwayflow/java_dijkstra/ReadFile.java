package SubWay2;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import SubWay2.Station;

public class ReadFile {
	//集合保存所有线路及该线路的站点信息
	public static Set<List<Station>> lineSet = new HashSet<List<Station>>();
	//所有站点数
    public static int totalStation = 0;
     //文件读取函数  
	public static void readText(){
		Station Prevstation = new Station();
        try {
            File file=new File("1.txt");
            //判断文件是否存在
            if(file.isFile() && file.exists()){ 
                InputStreamReader reader = new InputStreamReader(new FileInputStream(file));
                BufferedReader bufferedReader = new BufferedReader(reader);
                String stationline = null;
              
                int flag = 0;
                while((stationline = bufferedReader.readLine()) != null){
                    String[] tmp = stationline.split(" ");//分割符号，将空格置空
                    List<Station> Linestations = new ArrayList<Station>();//设置一个链表保存线路信息
                	for(int j=1;j<tmp.length;j++) {
                		Station station = new Station();
                		station.setLinename(tmp[0]);//将每一行的第一个字符串存入线路名
                		station.setName(tmp[j]);//保存站点名称
                        // System.out.print(tmp[j]);
                		Linestations.add(station);//保存线路信息
                		totalStation++;//计算总站点数
                		if(flag != 0) {//当flag不为零时，存在前后站点
                			station.prevsation = Prevstation;
                			Prevstation.nextsation = station;
                		}
                		Prevstation = station;//记录从零开始记录的站点
                		flag++;
                	}
                	lineSet.add(Linestations);//添加为线路集
                }
               // 关闭文件
                reader.close();
                bufferedReader.close();
            }
            else
                System.out.println("找不到指定的文件!");
          } catch (Exception e) {
              System.out.println("文件内容出错!");
              e.printStackTrace();
           }        
        }
	 
}





