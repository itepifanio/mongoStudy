package javaapplication.util;

import org.bson.Document;
import org.bson.codecs.DocumentCodec;
import org.bson.codecs.EncoderContext;
import org.bson.json.JsonMode;
import org.bson.json.JsonWriter;
import org.bson.json.JsonWriterSettings;

import java.io.StringWriter;

public class Helpers {
    public static void printJson(Document document) {
        JsonWriter jsonWriter = new JsonWriter(new StringWriter(),
                                               new JsonWriterSettings(JsonMode.SHELL, true));
        new DocumentCodec().encode(jsonWriter, document,
                                   EncoderContext.builder()
                                                 .isEncodingCollectibleDocument(true)
                                                 .build());
        System.out.println(jsonWriter.getWriter());
        // System.out.println();
        System.out.flush();
    }
}
