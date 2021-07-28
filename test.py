    def from_pic(self):
        self.thread_run = False
        self.pic_path = askopenfilename(title="选择识别图片", filetypes=[("jpg图片", "*.jpg"), ("png图片", "*.png")])
        if self.pic_path:
            # print('路径：',self.pic_path)
            img_bgr = predict.imreadex(self.pic_path)
            self.imgtk = self.get_imgtk(img_bgr)
            self.image_ctl.configure(image=self.imgtk)
            resize_rates = (1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4)
            for resize_rate in resize_rates:
                # print("resize_rate:", resize_rate)
                r, roi, color = self.predictor.predict(self.pic_path, resize_rate)
                print('99999999999999999999999', resize_rate, '888', r, roi, color)
                if r:
                    self.show_roi(r, roi, color)
                    break
