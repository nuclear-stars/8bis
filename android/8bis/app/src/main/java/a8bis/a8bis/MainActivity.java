package a8bis.a8bis;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        String username = getPreferences(Context.MODE_PRIVATE).getString(getString(R.string.username_setting), "");
        if (username.length() > 0) {
            // Username is already set, move
            this.moveToRestaurants(username);
        }
    }

    private void moveToRestaurants(String username) {
        Intent k = new Intent(this, RestaurantsActivity.class);
        k.putExtra(getString(R.string.username_setting), username);
        startActivity(k);
        finish();
    }

    public void onNextPressed(View view) {
        EditText edit = (EditText)findViewById(R.id.usernameText);
        String username = edit.getText().toString();

        if (username.length() < 3 || username.length() > 25) {
            Context context = getApplicationContext();
            Toast toast = Toast.makeText(
                    context, getString(R.string.username_3_25_chars), Toast.LENGTH_SHORT
            );
            toast.show();
            return;
        }

        SharedPreferences sharedPref = getPreferences(Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPref.edit();
        editor.putString(getString(R.string.username_setting), username);
        editor.apply();

        this.moveToRestaurants(username);
    }
}
