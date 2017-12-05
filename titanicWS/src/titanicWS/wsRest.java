package titanicWS;

import java.io.IOException;

import javax.enterprise.context.RequestScoped;
import javax.inject.Inject;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;

import rwk.ejbStateful;

@Path("/")
@RequestScoped
public class wsRest {
    
    @Inject 
    private ejbStateful sbsl;
    
    @GET
    @Path("/prediction")
    @Produces("text/plain")
    public String runSimulation(
    		@QueryParam("Pclass") String Pclass,
    		@QueryParam("Sex") String Sex,
    		@QueryParam("SibSp") String SibSp,
    		@QueryParam("Parch") String Parch) throws IOException {
        
        //return sbsl.getPrediction(value);
        return sbsl.runSimulation(Pclass, Sex, SibSp, Parch);
    }        
}