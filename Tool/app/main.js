"use strict";

const electron = require("electron");
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
let mainWindow;

// 全てのウィンドウが閉じたら終了
app.on('window-all-closed', function() {
  if (process.platform != 'darwin') {
    app.quit();
  }
});

// Electronの初期化完了後に実行
app.on('ready', function() {
  // メイン画面の表示。ウィンドウの幅、高さを指定できる
  mainWindow = new BrowserWindow({
        // ウィンドウ作成時のオプション
        "width": 900,
        "height": 250,
        "alwaysOnTop": true,
        "transparent": true,    // ウィンドウの背景を透過
        "frame": false,     // 枠の無いウィンドウ
        "resizable": false  // ウィンドウのリサイズを禁止
  });
  mainWindow.loadURL('file://' + __dirname + '/index.html');

  // ウィンドウが閉じられたらアプリも終了
  mainWindow.on('closed', function() {
    mainWindow = null;
  });
});