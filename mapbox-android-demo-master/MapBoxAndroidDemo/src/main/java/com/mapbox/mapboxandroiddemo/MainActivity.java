package com.mapbox.mapboxandroiddemo;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GooglePlayServicesUtil;
import com.google.android.gms.common.Scopes;
import com.google.android.gms.common.SignInButton;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.Scope;
import com.google.android.gms.plus.Plus;
import com.google.android.gms.plus.model.people.Person;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentSender;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Bundle;
import android.provider.Settings;
import android.support.v7.app.ActionBarActivity;
import android.support.v7.widget.CardView;
import android.support.v7.widget.GridLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.text.TextUtils;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.crashlytics.android.Crashlytics;
import com.mapbox.mapboxsdk.api.ILatLng;
import com.mapbox.mapboxsdk.geometry.BoundingBox;
import com.mapbox.mapboxsdk.geometry.LatLng;
import com.mapbox.mapboxsdk.overlay.Icon;
import com.mapbox.mapboxsdk.overlay.Marker;
import com.mapbox.mapboxsdk.overlay.UserLocationOverlay;
import com.mapbox.mapboxsdk.tileprovider.tilesource.*;
import com.mapbox.mapboxsdk.views.MapView;
import com.mapbox.mapboxsdk.views.util.TilesLoadedListener;

import java.util.ArrayList;

public class MainActivity extends ActionBarActivity implements
    View.OnClickListener,
    GoogleApiClient.ConnectionCallbacks,
    GoogleApiClient.OnConnectionFailedListener {

    private static final String TAG = "MainActivity";

    /* RequestCode for resolutions involving sign-in */
    private static final int RC_SIGN_IN = 9001;

    /* Keys for persisting instance variables in savedInstanceState */
    private static final String KEY_IS_RESOLVING = "is_resolving";
    private static final String KEY_SHOULD_RESOLVE = "should_resolve";

    /* Client for accessing Google APIs */
    private GoogleApiClient mGoogleApiClient;

    /* View to display current status (signed-in, signed-out, disconnected, etc) */
    private TextView mStatus;

    /* Is there a ConnectionResult resolution in progress? */
    private boolean mIsResolving = false;

    /* Should we automatically resolve ConnectionResults when possible? */
    private boolean mShouldResolve = false;

    private MapView mv;
	private UserLocationOverlay myLocationOverlay;
	private String currentMap = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Crashlytics.start(this);

        setContentView(R.layout.activity_main);

        mv = (MapView) findViewById(R.id.mapview);
		mv.setMinZoomLevel(mv.getTileProvider().getMinimumZoomLevel());
		mv.setMaxZoomLevel(mv.getTileProvider().getMaximumZoomLevel());
		mv.setCenter(mv.getTileProvider().getCenterCoordinate());
		mv.setZoom(0);
		currentMap = getString(R.string.streetMapId);

		// Show user location (purposely not in follow mode)
        mv.setUserLocationEnabled(true);
        mv.setUserLocationTrackingMode(UserLocationOverlay.TrackingMode.FOLLOW);
        mv.setUserLocationRequiredZoom(10);

        mv.loadFromGeoJSONURL("https://gist.githubusercontent.com/tmcw/10307131/raw/21c0a20312a2833afeee3b46028c3ed0e9756d4c/map.geojson");

//        setButtonListeners();
//        Marker m = new Marker(mv, "Edinburgh", "Scotland", new LatLng(55.94629, -3.20777));
//        m.setIcon(new Icon(this, Icon.Size.SMALL, "marker-stroked", "ee8a65"));
//        mv.addMarker(m);
//
//        m = new Marker(mv, "Stockholm", "Sweden", new LatLng(59.32995, 18.06461));
//        m.setIcon(new Icon(this, Icon.Size.LARGE, "city", "3887be"));
//        mv.addMarker(m);
//
//        m = new Marker(mv, "Prague", "Czech Republic", new LatLng(50.08734, 14.42112));
//        m.setIcon(new Icon(this, Icon.Size.MEDIUM, "land-use", "3bb2d0"));
//        mv.addMarker(m);
//
//        m = new Marker(mv, "Athens", "Greece", new LatLng(37.97885, 23.71399));
//        mv.addMarker(m);
//
//        m = new Marker(mv, "Tokyo", "Japan", new LatLng(35.70247, 139.71588));
//        m.setIcon(new Icon(this, Icon.Size.LARGE, "city", "3887be"));
//        mv.addMarker(m);
//
//        m = new Marker(mv, "Ayacucho", "Peru", new LatLng(-13.16658, -74.21608));
//        m.setIcon(new Icon(this, Icon.Size.LARGE, "city", "3887be"));
//        mv.addMarker(m);
//
//        m = new Marker(mv, "Nairobi", "Kenya", new LatLng(-1.26676, 36.83372));
//        m.setIcon(new Icon(this, Icon.Size.LARGE, "city", "3887be"));
//        mv.addMarker(m);
//
//        m = new Marker(mv, "Canberra", "Australia", new LatLng(-35.30952, 149.12430));
//        m.setIcon(new Icon(this, Icon.Size.LARGE, "city", "3887be"));
//        mv.addMarker(m);
//
//        m = new Marker(mv, "Maputo", "Mozambique", new LatLng(-5.26676, 47.83745));
//        m.setIcon(new Icon(this, Icon.Size.LARGE, "city", "3887be"));
//        mv.addMarker(m);

        mv.setOnTilesLoadedListener(new TilesLoadedListener() {
            @Override
            public boolean onTilesLoaded() {
                return false;
            }

            @Override
            public boolean onTilesLoadStarted() {
                // TODO Auto-generated method stub
                return false;
            }
        });
//        mv.setVisibility(View.VISIBLE);

        // Restore from saved instance state
        // [START restore_saved_instance_state]
        if (savedInstanceState != null) {
            mIsResolving = savedInstanceState.getBoolean(KEY_IS_RESOLVING);
            mShouldResolve = savedInstanceState.getBoolean(KEY_SHOULD_RESOLVE);
        }
        // [END restore_saved_instance_state]

        // Set up button click listeners
        findViewById(R.id.sign_in_button).setOnClickListener(this);
//        findViewById(R.id.sign_out_button).setOnClickListener(this);
//        findViewById(R.id.disconnect_button).setOnClickListener(this);

        // Large sign-in
        ((SignInButton) findViewById(R.id.sign_in_button)).setSize(SignInButton.SIZE_WIDE);

        // Start with sign-in button disabled until sign-in either succeeds or fails
//        findViewById(R.id.sign_in_button).setEnabled(false);

        // Set up view instances

        // [START create_google_api_client]
        // Build GoogleApiClient with access to basic profile
        mGoogleApiClient = new GoogleApiClient.Builder(this)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .addApi(Plus.API)
                .addScope(new Scope(Scopes.PROFILE))
                .build();
        // [END create_google_api_client]

	}

//    private void initializeData(){
//        appBundle = new ArrayList<>();
//        String largeText;
//        String smallText;
////        Drawable textLogo = context.getDrawable(findViewById(R.id.app_icon));
//
////        appBundle.add(new Login(, "Your Text Here", "Smaller text here"));
//    }
//
//    private void initializeAdapter(){
//        AppListAdapter adapter = new AppListAdapter(appBundle);
//        rv.setAdapter(adapter);
//    }

//	@Override
//	public boolean onCreateOptionsMenu(Menu menu)
//	{
//		MenuInflater menuInflater = getMenuInflater();
//		menuInflater.inflate(R.menu.menu_activity_main, menu);
//		return super.onCreateOptionsMenu(menu);
//	}
//
//	@Override
//	public boolean onOptionsItemSelected(MenuItem item)
//	{
//		switch (item.getItemId()) {
//			case R.id.menuItemStreets:
//				replaceMapView(getString(R.string.streetMapId));
//				return true;
//			case R.id.menuItemSatellite:
//				replaceMapView(getString(R.string.satelliteMapId));
//				return true;
//			case R.id.menuItemTerrain:
//				replaceMapView(getString(R.string.terrainMapId));
//				return true;
//			case R.id.menuItemOutdoors:
//				replaceMapView(getString(R.string.outdoorsMapId));
//				return true;
//			case R.id.menuItemWoodcut:
//				replaceMapView(getString(R.string.woodcutMapId));
//				return true;
//			case R.id.menuItemPencil:
//				replaceMapView(getString(R.string.pencilMapId));
//				return true;
//			case R.id.menuItemSpaceship:
//				replaceMapView(getString(R.string.spaceShipMapId));
//				return true;
//			default:
//				return super.onOptionsItemSelected(item);
//		}
//	}

    protected void replaceMapView(String layer) {

		if (TextUtils.isEmpty(layer) || TextUtils.isEmpty(currentMap) || currentMap.equalsIgnoreCase(layer)) {
			return;
		}

        ITileLayer source;
        BoundingBox box;

        source = new MapboxTileLayer(layer);

        mv.setTileSource(source);
        box = source.getBoundingBox();
        mv.setScrollableAreaLimit(box);
        mv.setMinZoomLevel(mv.getTileProvider().getMinimumZoomLevel());
        mv.setMaxZoomLevel(mv.getTileProvider().getMaximumZoomLevel());
		currentMap = layer;

        mv.setCenter(mv.getTileProvider().getCenterCoordinate());
        mv.setZoom(0);

    }

    private Button changeButtonTypeface(Button button) {
        return button;
    }

    public LatLng getMapCenter() {
        return mv.getCenter();
    }

    public void setMapCenter(ILatLng center) {
        mv.setCenter(center);
    }

    /**
     * Method to show settings  in alert dialog
     * On pressing Settings button will lauch Settings Options - GPS
     */
    public void showSettingsAlert() {
        AlertDialog.Builder alertDialog = new AlertDialog.Builder(getBaseContext());

        // Setting Dialog Title
        alertDialog.setTitle("GPS settings");

        // Setting Dialog Message
        alertDialog.setMessage("GPS is not enabled. Do you want to go to settings menu?");

        // On pressing Settings button
        alertDialog.setPositiveButton("Settings", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int which) {
                Intent intent = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS);
                getBaseContext().startActivity(intent);
            }
        });

        // on pressing cancel button
        alertDialog.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int which) {
                dialog.cancel();
            }
        });

        // Showing Alert Message
        alertDialog.show();
    }

    private void updateUI(boolean isSignedIn) {
        if (isSignedIn) {
            // Show signed-in user's name
            Person currentPerson = Plus.PeopleApi.getCurrentPerson(mGoogleApiClient);
            if (currentPerson != null) {
                String name = currentPerson.getDisplayName();
//                mStatus.setText(getString(R.string.signed_in_fmt, name));
            } else {
                Log.w(TAG, getString(R.string.error_null_person));
//                mStatus.setText(getString(R.string.signed_in_err));
            }

            // Set button visibility
            findViewById(R.id.sign_in_button).setVisibility(View.GONE);
            findViewById(R.id.sign_in_button).setVisibility(View.VISIBLE); // sign_out_and_disconnect
        } else {
            // Show signed-out message
//            mStatus.setText(R.string.signed_out);

            // Set button visibility
            findViewById(R.id.sign_in_button).setEnabled(true);
            findViewById(R.id.sign_in_button).setVisibility(View.VISIBLE);
            findViewById(R.id.sign_in_button).setVisibility(View.GONE); // sign_out_and_disconnect
        }
    }

    // [START on_start_on_stop]
    @Override
    protected void onStart() {
        super.onStart();
        mGoogleApiClient.connect();
    }

    @Override
    protected void onStop() {
        super.onStop();
        mGoogleApiClient.disconnect();
    }
    // [END on_start_on_stop]

    // [START on_save_instance_state]
    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putBoolean(KEY_IS_RESOLVING, mIsResolving);
        outState.putBoolean(KEY_SHOULD_RESOLVE, mShouldResolve);
    }
    // [END on_save_instance_state]

    // [START on_activity_result]
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        Log.d(TAG, "onActivityResult:" + requestCode + ":" + resultCode + ":" + data);

        if (requestCode == RC_SIGN_IN) {
            // If the error resolution was not successful we should not resolve further.
            if (resultCode != RESULT_OK) {
                mShouldResolve = false;
            }

            mIsResolving = false;
            mGoogleApiClient.connect();
        }
    }
    // [END on_activity_result]

    @Override
    public void onConnected(Bundle bundle) {
        // onConnected indicates that an account was selected on the device, that the selected
        // account has granted any requested permissions to our app and that we were able to
        // establish a service connection to Google Play services.
        Log.d(TAG, "onConnected:" + bundle);
        mShouldResolve = false;

        // Show the signed-in UI
        updateUI(false);
    }

    @Override
    public void onConnectionSuspended(int i) {
        // The connection to Google Play services was lost. The GoogleApiClient will automatically
        // attempt to re-connect. Any UI elements that depend on connection to Google APIs should
        // be hidden or disabled until onConnected is called again.
        Log.w(TAG, "onConnectionSuspended:" + i);
    }

    // [START on_connection_failed]
    @Override
    public void onConnectionFailed(ConnectionResult connectionResult) {
        // Could not connect to Google Play Services.  The user needs to select an account,
        // grant permissions or resolve an error in order to sign in. Refer to the javadoc for
        // ConnectionResult to see possible error codes.
        Log.d(TAG, "onConnectionFailed:" + connectionResult);

//        initMarks();

        if (!mIsResolving && mShouldResolve) {
            if (connectionResult.hasResolution()) {
                try {
                    connectionResult.startResolutionForResult(this, RC_SIGN_IN);
                    mIsResolving = true;
                } catch (IntentSender.SendIntentException e) {
                    Log.e(TAG, "Could not resolve ConnectionResult.", e);
                    mIsResolving = false;
                    mGoogleApiClient.connect();
                }
            } else {
                // Could not resolve the connection result, show the user an
                // error dialog.
                showErrorDialog(connectionResult);
            }
        } else {
            // Show the signed-out UI
//            showSignedOutUI();
        }
    }
    // [END on_connection_failed]

    private void showErrorDialog(ConnectionResult connectionResult) {
        int errorCode = connectionResult.getErrorCode();

        if (GooglePlayServicesUtil.isUserRecoverableError(errorCode)) {
            // Show the default Google Play services error dialog which may still start an intent
            // on our behalf if the user can resolve the issue.
            GooglePlayServicesUtil.getErrorDialog(errorCode, this, RC_SIGN_IN,
                    new DialogInterface.OnCancelListener() {
                        @Override
                        public void onCancel(DialogInterface dialog) {
                            mShouldResolve = false;
                            updateUI(false);
                        }
                    }).show();
        } else {
            // No default Google Play Services error, display a message to the user.
            String errorString = getString(R.string.play_services_error_fmt, errorCode);
            Toast.makeText(this, errorString, Toast.LENGTH_SHORT).show();

            mShouldResolve = false;
            updateUI(false);
        }
    }

    private void onSignInClicked() {
        // User clicked the sign-in button, so begin the sign-in process and automatically
        // attempt to resolve any errors that occur.
        mShouldResolve = true;
        mGoogleApiClient.connect();

        // Show a message to the user that we are signing in.
//        mStatus.setText(R.string.signing_in);
    }

    @Override
    public void onClick(View v) {
        if (v.getId() == R.id.sign_in_button) {
            onSignInClicked();
        }

        switch (v.getId()) {
            case R.id.sign_in_button:
                // User clicked the sign-in button, so begin the sign-in process and automatically
                // attempt to resolve any errors that occur.
//                mStatus.setText(R.string.signing_in);
                // [START sign_in_clicked]
                mShouldResolve = true;
                mGoogleApiClient.connect();

                initMarks();

                // [END sign_in_clicked]
                break;
//            case -123: //R.id.sign_out_button
//                // Clear the default account so that GoogleApiClient will not automatically
//                // connect in the future.
//                // [START sign_out_clicked]
//                if (mGoogleApiClient.isConnected()) {
//                    Plus.AccountApi.clearDefaultAccount(mGoogleApiClient);
//                    mGoogleApiClient.disconnect();
//                }
//                // [END sign_out_clicked]
//                updateUI(false);
//                break;
//            case R.id.disconnect_button:
//                // Revoke all granted permissions and clear the default account.  The user will have
//                // to pass the consent screen to sign in again.
//                // [START disconnect_clicked]
//                if (mGoogleApiClient.isConnected()) {
//                    Plus.AccountApi.clearDefaultAccount(mGoogleApiClient);
//                    Plus.AccountApi.revokeAccessAndDisconnect(mGoogleApiClient);
//                    mGoogleApiClient.disconnect();
//                }
//                // [END disconnect_clicked]
//                updateUI(false);
//                break;
        }
    }

    private void initMarks(){

        CardView cv = (CardView) findViewById(R.id.cardsignview);
        cv.setVisibility(CardView.GONE);

        Marker m = new Marker(mv, "Waterloo", "Canada", new LatLng(43.4667, -80.5167));
        m.setIcon(new Icon(this, Icon.Size.SMALL, "marker-stroked", "ee8a65"));
        mv.addMarker(m);

        m = new Marker(mv, "Toronto", "Canada", new LatLng(43.7000, -79.4000));
        m.setIcon(new Icon(this, Icon.Size.LARGE, "city", "3887be"));
        mv.addMarker(m);

        m = new Marker(mv, "Kingston", "Canada", new LatLng(44.2333, -76.5000));
        m.setIcon(new Icon(this, Icon.Size.LARGE, "city", "3887be"));
        mv.addMarker(m);
    }
}
