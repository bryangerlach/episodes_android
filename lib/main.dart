import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.black,             // Top status bar background
      statusBarIconBrightness: Brightness.light, // Top icons (clock/battery) white
      systemNavigationBarColor: Colors.black,     // Bottom navigation bar background
      systemNavigationBarIconBrightness: Brightness.light, // Bottom nav buttons white
    ),
  );

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Episodes',
      theme: ThemeData(
        scaffoldBackgroundColor: Colors.black, // Ensures background behind WebView is black
      ),
      home: const WebViewContainer(),
    );
  }
}

class WebViewContainer extends StatefulWidget {
  const WebViewContainer({super.key});

  @override
  State<WebViewContainer> createState() => _WebViewContainerState();
}

class _WebViewContainerState extends State<WebViewContainer> {
  late final WebViewController controller;
  String _url = "";

  @override
  void initState() {
    super.initState();
    controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..addJavaScriptChannel(
        'ThemeChannel',
        onMessageReceived: (JavaScriptMessage message) {
          // Listen for theme messages coming from your web app
          if (message.message == 'dark') {
            SystemChrome.setSystemUIOverlayStyle(
              const SystemUiOverlayStyle(
                statusBarColor: Colors.black,
                statusBarIconBrightness: Brightness.light, // White clock/icons
                systemNavigationBarColor: Colors.black,
                systemNavigationBarIconBrightness: Brightness.light,
              ),
            );
          } else if (message.message == 'light') {
            SystemChrome.setSystemUIOverlayStyle(
              const SystemUiOverlayStyle(
                statusBarColor: Colors.white,
                statusBarIconBrightness: Brightness.dark, // Dark clock/icons
                systemNavigationBarColor: Colors.white,
                systemNavigationBarIconBrightness: Brightness.dark,
              ),
            );
          }
        },
      );
      
    _checkForSavedUrl();
  }

  Future<void> _checkForSavedUrl() async {
    final prefs = await SharedPreferences.getInstance();
    _url = prefs.getString('url') ?? "";
    if (_url.isEmpty) {
      if (mounted) _showUrlInputDialog();
    } else {
      controller.loadRequest(Uri.parse(_url));
    }
  }

  Future<void> _showUrlInputDialog() async {
    final urlController = TextEditingController(text: _url);
    await showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        title: const Text('Enter Server URL'),
        content: TextField(
          controller: urlController,
          decoration: const InputDecoration(
            hintText: 'https://your-server.com',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () {
              final input = urlController.text.trim();
              if (Uri.parse(input).hasAbsolutePath) {
                setState(() {
                  _url = input;
                });
                controller.loadRequest(Uri.parse(_url));
                _saveUrlToSharedPreferences(_url);
                Navigator.pop(context);
              } else {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Invalid URL. Please include http:// or https://'),
                  ),
                );
              }
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }

  Future<void> _saveUrlToSharedPreferences(String url) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('url', url);
  }

  @override
  Widget build(BuildContext context) {
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, result) async {
        if (didPop) return;
        if (await controller.canGoBack()) {
          controller.goBack();
        } else {
          SystemNavigator.pop();
        }
      },
      child: Scaffold(
        body: SafeArea(
          child: RefreshIndicator(
            onRefresh: () async => controller.reload(),
            child: WebViewWidget(controller: controller),
          ),
        ),
      ),
    );
  }
}