package mongodb.exercicios;

import java.util.ArrayList;
import java.util.List;

import org.bson.Document;
import org.bson.conversions.Bson;

import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;

import static mongodb.util.Helpers.printJson;


public class Exercicio1 
{
    public static void main( String[] args )
    {
        MongoClient client = new MongoClient();
        MongoDatabase database = client.getDatabase("exercicios");
        MongoCollection<Document> movies = database.getCollection("movies");
        
        // a)
        Bson filter = new Document("director", "Stanley Kubrick");
        List<Document> moviesDirectorKubrick = movies.find(filter).into(new ArrayList<Document>());
        for(Document movie : moviesDirectorKubrick) {
        	printJson(movie);
        }

        // b)
        filter = Filters.or(
        			Filters.eq("director", "Stanley Kubrick"),
        			Filters.eq("director", "Sergio Leone")
        		);
        List<Document> moviesDirectorKubrickLeone = movies.find(filter).into(new ArrayList<Document>());
        for(Document movie : moviesDirectorKubrickLeone) {
        	printJson(movie);
        }
        
        client.close();
        
    }
}
