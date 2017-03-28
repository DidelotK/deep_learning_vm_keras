# -*- coding: utf-8 -*-

from deep_learning import insert_in_dataset

if __name__ == '__main__':
	path_dataset = '../../dataset'

	insert_in_dataset('basil', '../../data_on_preparation/basil', path_dataset)
	insert_in_dataset('coriander', '../../data_on_preparation/coriander', path_dataset)
	insert_in_dataset('mint', '../../data_on_preparation/mint', path_dataset)
	insert_in_dataset('parsley', '../../data_on_preparation/parsley', path_dataset)
	insert_in_dataset('petunia', '../../data_on_preparation/petunia', path_dataset)
	insert_in_dataset('purslane', '../../data_on_preparation/purslaneflower', path_dataset)
	insert_in_dataset('sage', '../../data_on_preparation/sage', path_dataset)
	insert_in_dataset('sunflower', '../../data_on_preparation/sunflower', path_dataset)
	insert_in_dataset('thyme', '../../data_on_preparation/thyme', path_dataset)
