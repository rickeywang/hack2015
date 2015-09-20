package com.mapbox.mapboxandroiddemo;

import android.graphics.drawable.Drawable;

/**
 * Created by Alex on 2015-09-20.
 */
public class Login {
        private final Drawable appIconId;
        private final String largeText;
        private final String smallText;

    public Login(Drawable appIconId, String largeText, String smallText){
            this.appIconId = appIconId;
            this.largeText = largeText;
            this.smallText = smallText;
    }

    public String[] getAppInfo(){
        String appInfo[] = new String[2];
        appInfo[0] = largeText;
        appInfo[1] = smallText;

        return appInfo;
    }

    public Drawable getAppIcon(){
        return appIconId;
    }

}
