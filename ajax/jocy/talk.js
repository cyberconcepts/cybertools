/*
 * Copyright (c) 2009 Helmut Merz helmutm@cy55.de
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */


// $Id$


dojo.provide('jocy.talk');


dojo.declare('jocy.talk.Manager', null, {

    info: 'jocy.talk Manager',

    constructor: function(){
        this.connections = {};  // map URLs to connection objects
    },

    start: function(url, receiver, user, password) {
        url = url.replace(/\/$/, '');
        // TODO: close connection if already present
        var conn = new jocy.talk.Connection(url, receiver, user, password);
        this.connections[url] = conn;
        conn.init();
        conn.start();
    },

    send: function(url, data) {
    },

    close: function(url) {
    }

});

jocy.talk.manager = new jocy.talk.Manager();


dojo.declare('jocy.talk.Connection', null, {

    info: 'jocy.talk Connection',

    constructor: function(url, receiver, user, password) {
        this.url = url.replace(/\/$/, '');
        this.receiver = receiver;   // receive callback function
        this.user = user;
        this.password = password;
        this.initialized = false;
        this.clientId = '';     // id provided by server
    },

    init: function() {
        // request client id
        message = {request: 'start'};
        return dojo.xhrPost({
            url: this.url,
            postData: dojo.toJson(message),
            handleAs: 'json',
            load: dojo.hitch(this, function(response, ioArgs) {
                this.clientId = response.client_id;
            })
        });
    },

    start: function() {
        // start polling
    },

    close: function() {
    },

    send: function(resourcePath, data) {
        return dojo.xhrPost({
            url: this._setupUrl(resourcePath),
            load: dojo.hitch(this, function(response, ioArgs) {
                return this._callback(response, ioArgs);
            }),
            postData: dojo.toJson(data)
        });
    },

    // private methods

    _poll: function() {
    },

    _setupUrl: function(path) {
        slash = (path.charAt(0) == '/' ? '' : '/');
        return this.url + slash + path;
    },

    _alert: function(data) {
        alert(data);
    }
});
