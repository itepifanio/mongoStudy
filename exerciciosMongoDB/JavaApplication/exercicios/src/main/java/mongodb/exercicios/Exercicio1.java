package mongodb.exercicios;

import java.util.ArrayList;
import java.util.List;

import org.bson.Document;
import org.bson.conversions.Bson;

import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.Sorts;

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

        // c)       
        filter = Filters.and(
        			Filters.eq("genres", "Comedy"),
        			Filters.eq("year", 1991)
        		);
        List<Document> comedyFrom1991 = movies.find(filter).into(new ArrayList<Document>());
        System.out.println(comedyFrom1991.size());
        
        // e)        
        List<Document> maxTimeComedyFrom1991 = movies.find(filter).sort(Sorts.descending("runtime")).limit(1).into(new ArrayList<Document>());;
                
        for(Document movie : maxTimeComedyFrom1991) {
        	printJson(movie);
        }
        
        // f)       
        filter = Filters.and(
    			Filters.gt("year", 1990),
    			Filters.lt("year", 1999),
    			Filters.gt("imdb.rating", 8.5)
    		);
        
	    List<Document> ninetyYears = movies.find(filter).sort(Sorts.descending("title")).into(new ArrayList<Document>());
	    
	    for(Document movie : ninetyYears) {
        	printJson(movie);
        }
        
        client.close();
    }
}