package com.mapbox.mapboxandroiddemo;

import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.List;

/**
 * Created by Alex on 2015-09-20.
 */
public class AppListAdapter extends RecyclerView.Adapter<AppListAdapter.AppViewHolder> {
    private final List<Login> apps;

    public static class AppViewHolder extends RecyclerView.ViewHolder{
        TextView largeText;
        TextView smallText;
        ImageView appIcon;
        View appView;

        public AppViewHolder(View itemView){
            super(itemView);
            largeText = (TextView) itemView.findViewById(R.id.app_name);
            smallText = (TextView) itemView.findViewById(R.id.app_size);
            appIcon = (ImageView) itemView.findViewById(R.id.app_icon);
            appView = itemView;
        }
    }

    AppListAdapter(List<Login> apps) {
        this.apps = apps;
    }

    @Override
    public AppViewHolder onCreateViewHolder(ViewGroup viewGroup, int i){
        final LayoutInflater layoutInflater = LayoutInflater.from(viewGroup.getContext());
        final View v = layoutInflater.inflate(R.layout.signin_card, viewGroup, false);

        return new AppViewHolder(v);
    }

    @Override
    public void onBindViewHolder(AppViewHolder appViewHolder, int i){
        appViewHolder.appIcon.setImageDrawable(apps.get(i).getAppIcon());
        appViewHolder.largeText.setText(apps.get(i).getAppInfo()[0]);
        appViewHolder.smallText.setText(apps.get(i).getAppInfo()[1]);
    }

    @Override
    public int getItemCount(){
        return apps.size();
    }
}
