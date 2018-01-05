#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import os
import sys
import unittest

sys.path.append('/'.join((os.path.abspath(__file__).split('/')[:-3])))

from increasing import ProgressBar


class ProgressBarTest(unittest.TestCase):

    def setUp(self):

        self.basic_init_config = {'open_symbol': '[', 'prefix': '', 'fill_symbol': '=', 'unfill_symbol': ' ',
                                  'close_symbol': ']', 'type': 'basic', 'cols': 50, 'value': 0.0, 'suffix': ''}
        self.arrow_init_config = {'open_symbol': '[', 'prefix': '', 'fill_symbol': '=', 'unfill_symbol': ' ',
                                  'arrow_symbol': '>', 'close_symbol': ']', 'type': 'arrow', 'cols': 50, 'value': 0.0,
                                  'suffix': ''}
        self.shade_init_config = {'open_symbol': '|', 'prefix': '', 'fill_symbol': '█', 'unfill_symbol': '░',
                                  'close_symbol': '|', 'type': 'shade',
                                  'cols': 50, 'value': 0.0, 'suffix': ''}
        self.block_init_config = {'open_symbol': '|', 'suffix': '', 'cols': 50, 'value': 0.0, 'prefix': '',
                                  'close_symbol': '|', 'type': 'block'}
        self.rect_init_config = {'open_symbol': '|', 'prefix': '', 'fill_symbol': '■', 'unfill_symbol': ' ',
                                 'close_symbol': '|', 'type': 'rect', 'cols': 50, 'value': 0.0, 'suffix': ''}
        self.rotate_init_config = {'open_symbol': '', 'prefix': '', 'cnt': 0, 'suffix': '', 'done_symbol': 'ok',
                                   'is_done': False, 'close_symbol': '', 'type': 'rotate', 'cols': 50, 'value': 0.0}

        self.basic_val_0_cols_10_output = '[' + ' ' * 10 + ']\r\n'
        self.arrow_val_0_cols_10_output = '[' + '>' + ' ' * 9 + ']\r\n'
        self.shade_val_0_cols_10_output = '|' + '░'*10 + '|\r\n'
        self.block_val_0_cols_10_output = '|' + ' ' * 10 + '|\r\n'
        self.rect_val_0_cols_10_output = '|' + ' ' * 10 + '|\r\n'
        self.rotate_cnt_0_cols_10_output = '-\r\n'

        self.basic_val_1_cols_10_output = '[' + '=' * 10 + ']\r\n'
        self.arrow_val_1_cols_10_output = '[' + '=' * 10 + ']\r\n'
        self.shade_val_1_cols_10_output = '|' + '█'*10 + '|\r\n'
        self.block_val_1_cols_10_output = '|' + '█' * 10 + '|\r\n'
        self.rect_val_1_cols_10_output = '|' + '■' * 10 + '|\r\n'
        self.rotate_cnt_1_cols_10_output = '\\\r\n'

    def test_check_configs(self):
        """Test empty, basic, arrow, shade, block, rect, rotate configurations
        """
        p = ProgressBar([])
        configs = p._check_configs([{}, {'type': 'basic'}, {'type': 'arrow'}, {'type': 'shade'}, {'type': 'block'},
                                    {'type': 'rect'}, {'type': 'rotate'}])

        self.assertEqual(configs[0], self.basic_init_config)
        self.assertEqual(configs[1], self.basic_init_config)
        self.assertEqual(configs[2], self.arrow_init_config)
        self.assertEqual(configs[3], self.shade_init_config)
        self.assertEqual(configs[4], self.block_init_config)
        self.assertEqual(configs[5], self.rect_init_config)
        self.assertEqual(configs[6], self.rotate_init_config)

    def test_update_config_by_index(self):
        """ Test updating configurations.
        """
        data = {'value': 0.5, 'prefix': '*', 'suffix': '&', 'is_done': True}
        p = ProgressBar([{}])
        p._update_config_by_index(0, data)
        self.assertEqual(p._configs[0]['value'], data['value'])
        self.assertEqual(p._configs[0]['prefix'], data['prefix'])
        self.assertEqual(p._configs[0]['suffix'], data['suffix'])
        self.assertEqual(p._configs[0]['is_done'], data['is_done'])

    def test_render_output(self):
        """Test output at value 0 and value 1.
        """
        p = ProgressBar([{'cols': 10}, {'type': 'basic', 'cols': 10}, {'type': 'arrow', 'cols': 10},
                         {'type': 'shade', 'cols': 10}, {'type': 'block', 'cols': 10}, {'type': 'rect', 'cols': 10},
                         {'type': 'rotate', 'cols': 10}])
        self.assertEqual(p._render_output(), self.basic_val_0_cols_10_output + self.basic_val_0_cols_10_output +
                         self.arrow_val_0_cols_10_output + self.shade_val_0_cols_10_output +
                         self.block_val_0_cols_10_output + self.rect_val_0_cols_10_output +
                         self.rotate_cnt_0_cols_10_output)

        for i in range(7):
            p._update_config_by_index(i, {'value': 1})
        self.assertEqual(p._render_output(), self.basic_val_1_cols_10_output +
                         self.basic_val_1_cols_10_output + self.arrow_val_1_cols_10_output +
                         self.shade_val_1_cols_10_output + self.block_val_1_cols_10_output +
                         self.rect_val_1_cols_10_output + self.rotate_cnt_1_cols_10_output)
