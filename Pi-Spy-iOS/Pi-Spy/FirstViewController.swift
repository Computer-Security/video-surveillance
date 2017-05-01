//
//  FirstViewController.swift
//  Pi-Spy
//
//  Created by 彭铭仕 on 2/23/17.
//  Copyright © 2017 Home Surveillance Inc. All rights reserved.
//

import UIKit

class FirstViewController: UIViewController {

  @IBOutlet weak var datePickerTxt: UITextField!
  @IBOutlet weak var statusLabel: UILabel!
  @IBOutlet weak var upperBackground: UIView!

  let datePicker = UIDatePicker()

  override func viewDidLoad() {
    super.viewDidLoad()
    createDatePicker()
    NotificationCenter.default.addObserver(self, selector: #selector(self.statusBarActive), name: NSNotification.Name(rawValue: "Recording Activated"), object: nil)
    NotificationCenter.default.addObserver(self, selector: #selector(self.statusBarDeactive), name: NSNotification.Name(rawValue: "Recording Deactivated"), object: nil)
  }



  func createDatePicker() {
    // toolbar
    let toolbar = UIToolbar()
    toolbar.sizeToFit()

    // bar button item
    let doneButton = UIBarButtonItem(barButtonSystemItem: .done, target: nil, action: #selector(donePressed))
    toolbar.setItems([doneButton], animated: false)

    datePickerTxt.inputAccessoryView = toolbar

    // assigning date picker to text field
    datePicker.datePickerMode = .date
    datePickerTxt.inputView = datePicker
  }

  func donePressed() {

    // format date
    let dateFormatter = DateFormatter()
    dateFormatter.dateStyle = .short
    dateFormatter.timeStyle = .none

    datePickerTxt.text = dateFormatter.string(from: datePicker.date)
    self.view.endEditing(true)
  }

  func statusBarActive(notif: Notification) {
    self.statusLabel.text = "Recording Activated"
    self.statusLabel.backgroundColor = UIColor(red: 75/255, green: 214/255, blue: 98/255, alpha: 1)
    self.upperBackground.backgroundColor = UIColor(red: 75/255, green: 214/255, blue: 98/255, alpha: 1)
  }

  func statusBarDeactive(notif: Notification) {
    self.statusLabel.text = "Recording Deactivated"
    self.statusLabel.backgroundColor = UIColor(red: 255/255, green: 89/255, blue: 60/255, alpha: 1)
    self.upperBackground.backgroundColor = UIColor(red: 255/255, green: 89/255, blue: 60/255, alpha: 1)
  }

}
