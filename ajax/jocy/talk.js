/*
 * Copyright (c) 2010 Helmut Merz helmutm@cy55.de
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


dojo.declare('jocy.talk.Connection', null, {

    info: 'jocy.talk Connection',

    constructor: function() {
        this.receiver = null;
        this.polling = false;
        this.id = null;
    },

    open: function(receiver, id) {
        this.receiver = receiver;
        if (id != undefined) {
            this.id = id;
        } else {
            this._getid();
        }
        this._poll();
        return this.id;
    },

    close: function() {
        return dojo.xhrPost({
            url: '/.stop/' + this.id,
            load: dojo.hitch(this, function(response, ioArgs) {
                this.polling = false;
            })
        });
    },

    send: function(path, data) {
        return dojo.xhrPost({
            url: '/.send/' + this.id + path,
            postData: dojo.toJson(data)
        });
    },

    // private methods

    _getId: function() {
        return dojo.xhrPost({
            url: '/.getid',
            sync: true,
            load: dojo.hitch(this, function(response, ioArgs) {
                this.id = response;
            })
        });
    },

    _poll: function() {
        if (this.polling) {
            return;
        }
        if (this.id == undefined) {
            this._getId();
        }
        this.polling = true;
        return dojo.xhrPost({
            url: '/.poll/' + this.id,
            handleAs: 'json',
            error: dojo.hitch(this, this._handlePollError),
            load: dojo.hitch(this, this._handlePollResponse)
        });
    },

    _handlePollResponse: function(response, ioArgs) {
        if (!this.polling) {
            return;
        }
        this.polling = false;
        t = response.type;
        switch (response.type) {
            case 'stop':
                break;
            case 'idle':
                this._poll();
                break;
            case 'error':
                self.receiver(response.data);
                break;
            case 'data':
                this._poll();
                self.receiver(response.data);
                break;
            default:
                this.poll();
        }
    },

    _handlePollError: function(response, ioArgs) {
        if (!this.polling) {
            return;
        }
        this.polling = false;
        this._poll();
    }
});

jocy.talk.connection = new jocy.talk.Connection();
