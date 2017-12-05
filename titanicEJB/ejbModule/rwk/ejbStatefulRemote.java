package rwk;

import java.io.IOException;

import javax.ejb.Remote;

@Remote
public interface ejbStatefulRemote {
	
	String runSimulation(String Pclass, String Sex, String SibSp, String Parch);
	
	String getPrediction() throws IOException;
	
	boolean createInputFile(String[] params);
	
}
