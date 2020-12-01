import os, os.path
import shutil

def clear_folder(folder):
	for file in os.listdir(folder):
	    file_path = os.path.join(folder, file)
	    try:
	        if os.path.isfile(file_path):
	            os.unlink(file_path)
	        elif os.path.isdir(file_path): 
	        	shutil.rmtree(file_path)
	    except Exception as e:
	        print(e)

def move_folder2folder(source_folder, destination_folder):
	# list sub_folder trong folder đích
	source_directorys = os.listdir(source_folder)
	#list sub_folder trong folder nguồn
	dest_directorys = os.listdir(destination_folder)

	# kiểm tra xem nếu folder đích rỗng
	if len(dest_directorys) == 0:
		# duyệt tất cả file trong folder nguồn
		for source_directory in source_directorys:
			source_dir_path = os.path.join(source_folder, source_directory)
			# đếm số file ảnh trong folder
			start_name = 0
			# kiểm tra nếu đó là folder
			if os.path.isdir(source_dir_path):
				# tạo sub_folder trong folder đích có tên 
				# giống với các sub_folder trong folder nguồn
				dest_folder_dist = destination_folder + source_directory 
				os.makedirs(dest_folder_dist)
				# duyệt tất cả các file trong từng sub_folder 
				for f in os.listdir(source_dir_path):
					start_name += 1 
					new_file = ("%s.jpg" % start_name)
					old_path = os.path.join(source_dir_path, f)
					new_path = os.path.join(dest_folder_dist, new_file)
					# chuyển file sang sub_folder trong folder đích
					shutil.move(old_path, new_path)
	# kiểm tra nếu folder đích không rỗng
	else:
		# duyệt các sub_folder trong source_folder
		for source_directory in source_directorys:
			source_dir_path = os.path.join(source_folder, source_directory)
			isduplicate = False
			# duyệt tất cả các sub_folder trong dest_folder
			for dest_directory in dest_directorys:
				# kiểm tra nếu 2 sub_folder trùng nhau 
				if source_directory.lower() == dest_directory.lower():
					isduplicate = True
					# copy toàn bộ file trong sub_folder của source
					# sang sub_folder của destination
					#...
					#...
					dest_folder_dist = os.path.join(destination_folder, dest_directory)
					start_name = len(os.listdir(dest_folder_dist))
					for f in os.listdir(source_dir_path):
						start_name += 1 
						new_file = ("%s.jpg" % start_name)
						old_path = os.path.join(source_dir_path, f)
						new_path = os.path.join(dest_folder_dist, new_file)
						# chuyển file sang sub_folder trong folder đích
						shutil.move(old_path, new_path)


			# nếu dist_folder chưa tồn tại folder 
			# có trong source folder
			if not isduplicate:
				start_name = 0
				# tạo sub_folder trong dest_folder 
				dest_folder_dist = destination_folder + source_directory 
				os.makedirs(dest_folder_dist)
				# duyệt tất cả file trong sub_folder của source_folder
				# chuyển sang sub_folder của destination_folder
				for f in os.listdir(source_dir_path):
					start_name += 1 
					new_file = ("%s.jpg" % start_name)
					old_path = os.path.join(source_dir_path, f)
					new_path = os.path.join(dest_folder_dist, new_file)
					# chuyển file sang sub_folder trong folder đích
					shutil.move(old_path, new_path)

	# xóa tất cả file trong source_folder
	# cách 1:
	clear_folder(source_folder)
	# cách 2:
	# nhưng chỉ những empty folder mới xóa được
	# for source_directory in source_directorys:
	# 	sub_dir_path = os.path.join(source_folder, source_directory)
	# 	os.rmdir(sub_dir_path)