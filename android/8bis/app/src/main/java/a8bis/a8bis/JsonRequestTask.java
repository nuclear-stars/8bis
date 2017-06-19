package a8bis.a8bis;

import android.content.Context;
import android.os.AsyncTask;
import android.widget.Toast;

import org.json.JSONObject;

class JsonResponseTask extends AsyncTask<String, Void, JSONObject> {
    protected Context ctx;
    private Exception exception;

    public JsonResponseTask(Context ctx) {
        this.ctx = ctx;
    }

    protected JSONObject doInBackground(String... urls) {
        try {
            return JSONParser.getJSON(urls[0]);
        } catch (Exception e) {
            this.exception = e;

            return null;
        }
    }

    protected void onPostExecute(JSONObject jsonObject) {
        if (jsonObject == null) {
            Toast.makeText(
                    ctx,
                    "Network error. Please try again later",
                    Toast.LENGTH_SHORT
            ).show();
        }
    }
}
