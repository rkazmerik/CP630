package rwk;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import javax.ejb.LocalBean;
import javax.ejb.Stateful;


/**
 * Session Bean implementation class ejbStateful
 */
@Stateful
@LocalBean
public class ejbStateful implements ejbStatefulRemote {

    /**
     * Default constructor. 
     */
    public ejbStateful() {
        // TODO Auto-generated constructor stub
    }
    
    public String runSimulation(String Pclass, String Sex, String SibSp, String Parch) {
		
    	String[] params = {Pclass, Sex, SibSp, Parch};
		String result = "";
		
    	boolean ready = createInputFile(params);
    	
    	if(ready){
    		try {
				result = getPrediction();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
    	}
    	
    	return result;
    }
    
    @Override
    public String getPrediction() throws IOException {
    	
    	String output = "";
    
    	String cmd = "cmd /c spark-submit --master spark://10.211.55.3:7077 /Users/ryankazmerik/cp630/final/CP630/titanic.py";
    	
    	try {
			Process process = Runtime.getRuntime().exec(cmd);

			// Get input streams
			BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));
			
			// Read command standard output
			String s;
			System.out.println("Standard output: ");
			while ((s = stdInput.readLine()) != null) {
				if(s.contains("prediction=")){
					System.out.println(s);
					Integer pred = Integer.valueOf((s.substring(15, 16)));
					
					if(pred == 1){
						output= "You survived!";
					} else {
						output= "You did not survive!";
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace(System.err);
		}
    	
    	return output;
    }
    
    @Override
    public boolean createInputFile(String[] params){
		
    	String header = "Pclass,Survived,Sex,SibSp,Parch";
    	String values = params[0]+","+"0"+","+params[1]+","+params[2]+","+params[3];
    	boolean result = false;
    	
    	String content = header+"\n"+values;
    	
    	try {

			FileWriter fw = new FileWriter("c:\\Users\\ryankazmerik\\cp630\\final\\CP630\\data\\userInput.csv");
			BufferedWriter bw = new BufferedWriter(fw);
			bw.write(content);
			bw.close();
			result = true;
			
		} catch (IOException e) {
			e.printStackTrace();
		}
    	
    	return result;
 	
    }
}
