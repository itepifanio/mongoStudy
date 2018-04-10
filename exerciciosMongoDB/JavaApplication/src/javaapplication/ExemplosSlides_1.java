package javaapplication;

import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

import org.bson.Document;
import org.bson.conversions.Bson;

import static com.mongodb.client.model.Updates.set;
import static com.mongodb.client.model.Filters.gte;
import static com.mongodb.client.model.Filters.eq;
import static com.mongodb.client.model.Projections.excludeId;
import static com.mongodb.client.model.Projections.fields;
import static com.mongodb.client.model.Projections.include;
import static com.mongodb.client.model.Sorts.descending;
import static com.mongodb.client.model.Sorts.orderBy;
import static javaapplication.util.Helpers.printJson;

import java.util.ArrayList;
import java.util.List;

public class ExemplosSlides_1 {
	
    public static void main(String[] args) {
    	
    	//Insert (slide 13)
    	
        MongoClient client = new MongoClient();
        MongoDatabase db = client.getDatabase("mongodbpratica");
        MongoCollection<Document> coll = db.getCollection("insertCollection");
        coll.drop();

        Document renato = new Document("name", "Renato")
                         .append("age", 26)
                         .append("profession", "developer");

        Document maria = new Document("name", "Maria")
                         .append("age", 28)
                         .append("profession", "tester");
        
        coll.insertOne(renato);
        coll.insertOne(maria);
        
        List<Document> all = coll.find().into(new ArrayList<Document>());
        
        System.out.println(">>> RESULTADO DO SLIDE 13 <<<");
        for (Document cur : all) {
            printJson(cur);
        }
        
        //coll.insertMany(asList(renato, maria));
        
        //Find (slide 14)
        
        Document first = coll.find().first();
        System.out.println(">>> RESULTADO DO SLIDE 14 <<<");
        printJson(first);

        //Find (slide 15)
        
        Document jose = new Document("name", "Jos�")
                .append("age", 50)
                .append("profession", "software engineer");
        
        coll.insertOne(jose);
        
        List<Document> all2 = coll.find().into(new ArrayList<Document>());
        
        System.out.println(">>> RESULTADO DO SLIDE 15 <<<");
        for (Document cur : all2) {
            printJson(cur);
        }

        
        //Find (slide 16)
        
        Document marcio = new Document("name", "M�rcio")
                .append("age", 40)
                .append("profession", "developer");
        
        coll.insertOne(marcio);
        
        Bson filter = new Document("profession", "developer");
        List<Document> onlyDevelopers = coll.find(filter).into(new ArrayList<Document>());
        
        System.out.println(">>> RESULTADO DO SLIDE 16 <<<");
        for (Document cur : onlyDevelopers) {
            printJson(cur);
        }
        
        //Find (slide 17)
        
        Bson filter2 = new Document("profession", "developer").append("age", new Document("$lt", 28));
        List<Document> onlyDevelopersAgeLt28 = coll.find(filter2).into(new ArrayList<Document>());
        
        System.out.println(">>> RESULTADO DO SLIDE 17 <<<");
        for (Document cur : onlyDevelopersAgeLt28) {
            printJson(cur);
        }
        
        //Find (slide 18)
        
        //Bson sort = new Document("age", -1);
        Bson sort = orderBy(descending("age"));
        Bson projection = fields(include("name", "age"), excludeId());
        List<Document> all3 = coll.find().projection(projection).sort(sort).limit(3).into(new ArrayList<Document>());
        
        System.out.println(">>> RESULTADO DO SLIDE 18 <<<");
        for (Document cur : all3) {
            printJson(cur);
        }
        
        //Delete (slide 19)
        
        coll.deleteOne(eq("name", "Renato"));
        List<Document> all4 = coll.find().projection(projection).sort(sort).into(new ArrayList<Document>());

        System.out.println(">>> RESULTADO DO SLIDE 19 <<<");
        for (Document cur : all4) {
            printJson(cur);
        }
        
        //Update (slide 20)

        coll.updateOne(eq("name", "Maria"), set("age", 55));
        List<Document> all5 = coll.find().projection(projection).sort(sort).limit(3).into(new ArrayList<Document>());

        System.out.println(">>> RESULTADO DO SLIDE 20 <<<");
        for (Document cur : all5) {
            printJson(cur);
        }
        
        coll.updateMany(gte("age", 50), set("bonus", true));
        List<Document> all6 = coll.find().sort(sort).limit(3).into(new ArrayList<Document>());

        System.out.println(">>> RESULTADO DO SLIDE 21 <<<");
        for (Document cur : all6) {
            printJson(cur);
        }
    }
}
