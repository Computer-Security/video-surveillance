//
//  LoginViewController.swift
//  Pi-Spy
//
//  Created by 彭铭仕 on 4/6/17.
//  Copyright © 2017 Home Surveillance Inc. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON

class LoginViewController: UIViewController {
  @IBOutlet weak var username: UITextField!
  @IBOutlet weak var password: UITextField!

  @IBAction func screenTapped(_ sender: UITapGestureRecognizer) {
    self.view.endEditing(true)
  }

    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


  @IBAction func loginButtonPressed(_ sender: UIButton) {
    let parameters: Parameters = [
      "username": username.text!,
      "password": password.text!
  ]
    print(parameters)

    Alamofire.request("http://66.108.38.161:444/login", method: .post, parameters: parameters, encoding: URLEncoding.default).responseJSON() {
      response in
      /*
      print("Request:")
      print(response.request!)  // original URL request
      print("Response:")
      print(response.response!) // HTTP URL response
      print("data:")
      print(response.data!)     // server data
      print("result:")
      print(response.result)   // result of response serialization
      */
      if let json = response.result.value {
        print("JSON: \(json)")
        if let result = JSON(json)["result"].string {
          if  result == "success" {
            self.performSegue(withIdentifier: "loginSegue", sender: nil)
          }else {
            var err_message = "Log in failed"
            if let err = JSON(json)["error"].string {
              if "no user found" == err {
                err_message = "User Validation Failed!"
              } else if ("input not valid" == err) {
                err_message = "User input has illegal characters"
              }
            }
            let alertController = UIAlertController(title: err_message, message: "Please try again", preferredStyle: UIAlertControllerStyle.alert)
            alertController.addAction(UIAlertAction(title: "Dismiss", style: UIAlertActionStyle.default, handler: nil))
            self.present(alertController, animated: true, completion: nil)
          }
        }
      }
    }

  }

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
