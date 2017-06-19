package a8bis.a8bis;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.CompoundButton;
import android.widget.Switch;
import android.widget.TextView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class RestaurantsActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_restaurants);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.setDrawerListener(toggle);
        toggle.syncState();

        Switch isVegan = (Switch) findViewById(R.id.isVegan);
        isVegan.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {

            }
        });

        TextView usernameLabel = (TextView)findViewById(R.id.usernameLabel);
        usernameLabel.setText(getIntent().getStringExtra(getString(R.string.username_setting)));

        getRestaurantsList();
    }

    // TODO: Move to a different class for sidebar
    public void onLogout(View view) {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);

        SharedPreferences.Editor editor = getPreferences(Context.MODE_PRIVATE).edit();
        editor.putString(getString(R.string.username_setting), "");
        editor.apply();

        Intent k = new Intent(this, MainActivity.class);
        startActivity(k);
        finish();
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    private void getRestaurantsList() {
        new JsonResponseTask(getApplicationContext()) {
            @Override
            protected void onPostExecute(JSONObject jsonObject) {
                super.onPostExecute(jsonObject);
                if (jsonObject == null) return;

                try {
                    ViewGroup restViewGroup = (ViewGroup) findViewById(R.id.layout_restaurants);
                    restViewGroup.removeAllViews();

                    JSONArray jsonArr = jsonObject.getJSONArray("restaurants");
                    for (int i = 0; i < jsonArr.length(); ++i) {
                        String restaurantName = jsonArr.getString(i);
                        View restLayout = LayoutInflater.from(RestaurantsActivity.this)
                                .inflate(R.layout.layout_restaurant, restViewGroup, false);
                        ((TextView) restLayout.findViewById(R.id.restaurant_name)).setText(restaurantName);
                        restViewGroup.addView(restLayout);
                    }
                } catch (JSONException e) {
                    Toast.makeText(
                            ctx,
                            "Failed to read restaurants. Please try again later",
                            Toast.LENGTH_SHORT
                    ).show();
                }
            }
        }.execute("/restaurants");
    }
}
