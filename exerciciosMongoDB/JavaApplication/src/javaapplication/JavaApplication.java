package javaapplication;

import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;

/**
 *
 * @author itepifanio
 */
public class JavaApplication {
    public static void main(String[] args) {
        MongoClient client = new MongoClient();
        // Cria banco, caso ele ainda não exista
        MongoDatabase database = client.getDatabase("app");
        MongoCollection<Document> collection = database.getCollection("appCollection");
        
        collection.drop();
        
        for(int i = 0; i < 10; i++){
            collection.insertOne(new Document("x", i));
        }
        
        System.out.println(collection.count());
    } 
}
