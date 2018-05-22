package mongodb.exercicios;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.bson.Document;
import org.bson.conversions.Bson;

import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Accumulators;
import com.mongodb.client.model.Aggregates;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.Sorts;

import static mongodb.util.Helpers.printJson;

public class Exercicio2 {
	public static void main( String[] args ) {
		MongoClient client = new MongoClient();
        MongoDatabase database = client.getDatabase("class");
        MongoCollection<Document> movies = database.getCollection("grades");
        
        // a)
        List<Document> filteredMovies = movies.aggregate(
        	(List<? extends Bson>)
        	Arrays.asList(
        		Aggregates.group("$student_id", Accumulators.sum("maiorMedia", "$score")),
        		Aggregates.group("$student_id", Accumulators.max("maxMedia", "$maiorMedia"))
        	)
        ).into(new ArrayList<Document>());
        	
        for(Document movie : filteredMovies) {
        	printJson(movie);
        }
        
        // b)
        /*db.grades.aggregate([{$match:{type:"homework"}}, { $group: { _id: "$student_id", topScore: { $max : "$score"}}}, {$sort:{_id:-1}}])*/
        List<Document> topScore = movies.aggregate(
            	(List<? extends Bson>)
            	Arrays.asList(
            		Aggregates.match(Filters.eq("type", "homework")),
            		Aggregates.group("$student_id", Accumulators.max("topScore", "$score")),
            		Aggregates.sort(Sorts.descending("_id"))
            	)
            ).into(new ArrayList<Document>());
            	
            for(Document movie : topScore) {
            	printJson(movie);
            }
        
        client.close();
	}
}
