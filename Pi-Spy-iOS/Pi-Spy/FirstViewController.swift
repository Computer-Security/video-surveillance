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
  let datePicker = UIDatePicker();
  
  override func viewDidLoad() {
    super.viewDidLoad()
    createDatePicker()
  }


  
  func createDatePicker(){
    // toolbar
    let toolbar = UIToolbar();
    toolbar.sizeToFit();
    
    // bar button item
    let doneButton = UIBarButtonItem(barButtonSystemItem: .done, target: nil, action: #selector(donePressed))
    toolbar.setItems([doneButton], animated: false)
    
    datePickerTxt.inputAccessoryView = toolbar
    
    // assigning date picker to text field
    datePicker.datePickerMode = .date
    datePickerTxt.inputView = datePicker
  }
  
  func donePressed(){
    
    // format date
    let dateFormatter = DateFormatter()
    dateFormatter.dateStyle = .short
    dateFormatter.timeStyle = .none
    
    datePickerTxt.text = dateFormatter.string(from: datePicker.date)
    self.view.endEditing(true);
  }
}

