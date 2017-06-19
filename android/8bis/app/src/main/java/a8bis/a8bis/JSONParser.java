package a8bis.a8bis;

/**
 * Created by omerp on 19/06/2017.
 */

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONException;
import org.json.JSONObject;

import android.util.Log;

public class JSONParser {
    private static String SERVER_URL = "http://13.93.107.254/webservice";

    public static JSONObject getJSON(String path) throws JSONException {
        return getJSONFromUrl(SERVER_URL + path);
    }

    private static JSONObject getJSONFromUrl(String url) throws JSONException {
        JSONObject jObj;
        InputStream is = null;
        String json = "";

        // Making HTTP request
        try {
            // defaultHttpClient
            DefaultHttpClient httpClient = new DefaultHttpClient();
            HttpPost httpPost = new HttpPost(url);

            HttpResponse httpResponse = httpClient.execute(httpPost);
            HttpEntity httpEntity = httpResponse.getEntity();
            is = httpEntity.getContent();

        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
            throw new JSONException("UnsupportedEncodingException");
        } catch (ClientProtocolException e) {
            e.printStackTrace();
            throw new JSONException("ClientProtocolException");
        } catch (IOException e) {
            e.printStackTrace();
            throw new JSONException("IOException");
        }

        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(
                    is, "utf-8"), 8);
            StringBuilder sb = new StringBuilder();
            String line = null;
            while ((line = reader.readLine()) != null) {
                sb.append(line + "n");
            }
            is.close();
            json = sb.toString();
        } catch (Exception e) {
            Log.e("Buffer Error", "Error converting result " + e.toString());
            throw new JSONException("Error converting result");
        }

        // return JSON String
        return new JSONObject(json);

    }
}
